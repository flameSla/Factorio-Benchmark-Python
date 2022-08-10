import re
import platform
from enum import Enum

import datetime
import shutil
import statistics
import subprocess
import psutil

############################################################################
def get_cpu_str( cpu ):
    if cpu == 0:
        return 'CPUxALL'
    else:
        return 'CPUx{0:02} '.format(cpu)
############################################################################
def get_avg(file_name, run, runs, cpu, benchmark_verbose):
    version = str()
    execution_time = str()
    avg = list()
    
    with open(file_name) as f:
        lines = f.read().split('\n')

    class Steps(Enum):
        VERSION_SEARCH = 1
        EXECUTION_TIME_SEARCH = 2
        AVG_SEARCH = 3
        RUN1_SEARCH = 4
        GET_COLUMNS = 5
        GET_VALUES = 6
        
    vals = list()
    columns = list()
    tick = 0
    step = Steps.VERSION_SEARCH
    for line in lines:
        if step == Steps.VERSION_SEARCH:
            result = re.search('; Factorio (\d+\.\d+\.\d+)', line)
            if result:
                version = result[1]
                step = Steps.EXECUTION_TIME_SEARCH
        elif step == Steps.EXECUTION_TIME_SEARCH:
            result = re.match('\s*Performed (\d*) updates in (\d*.\d* ms)', line)
            if result and result.lastindex == 2:
                execution_time = result[2]
                step = Steps.AVG_SEARCH
        elif step == Steps.AVG_SEARCH:
            result = re.match('\s*avg: (\d*.\d*) ms,', line)
            if result:
                a = float( result[1] )
                avg.append( a )
                print('run - {0}\t\t{1}\t{2:.2f} FPS\t{3}'.format(run, execution_time, 1000/a, get_cpu_str(cpu)))
                if len(avg) < runs:
                    step = Steps.EXECUTION_TIME_SEARCH
                else:
                    if benchmark_verbose is False:
                        break
                    else:
                        step = Steps.RUN1_SEARCH
        elif step == Steps.RUN1_SEARCH:
            if line == 'run 1:':
                step = Steps.GET_COLUMNS
        elif step == Steps.GET_COLUMNS:
            columns = line[0:-1].split(',')
            step = Steps.GET_VALUES
        elif step == Steps.GET_VALUES:
            if line[0] == 't':
                val = [float(i)/1000000.0 for i in line[1:-1].split(',')]
                if len(val) > len(vals):
                    vals = val
                else:
                    vals = list( map(sum, zip(vals,val)) )
                    
                tick = int( val[0] * 1000000.0 )
            else:
                tick += 1
                vals = [ i/tick for i in vals ]
                break

    return( [version, avg, columns, vals] )
############################################################################
def do_one_benchmark( save, ticks, run, runs, cpu, mod_directory, benchmark_verbose ):
    ret_value = list()

    if mod_directory == "":
        mod_directory = "temp_for_mod"
        try:
            shutil.rmtree( mod_directory )
        except OSError as e:
            pass

    argList = list()
    if platform.system() == 'Windows':
        argList.append('factorio.exe')
    elif platform.system() == 'Linux':
        argList.append('factorio')

    argList.append('--mod-directory')
    argList.append(mod_directory)
    argList.append('--benchmark')
    argList.append(save)
    argList.append('--benchmark-ticks')
    argList.append( str(ticks) )
    argList.append('--benchmark-runs')
    argList.append( str(runs) )
    argList.append('--disable-audio')
    if benchmark_verbose:
        argList.append('--benchmark-verbose')
        argList.append('all')
    
    process = psutil.Popen( args = argList, stdout=subprocess.PIPE, stderr=subprocess.PIPE )
    if platform.system() == 'Windows':
        process.nice( psutil.HIGH_PRIORITY_CLASS )
    elif platform.system() == 'Linux':
        process.nice( -20 )

    if cpu != 0:
        process.cpu_affinity(list(range(0,cpu)))

    out, err = process.communicate()
    if process.returncode != 0:
    # Error
        print( out )
        print( err )
    else:
        with open( 'temp', 'wb' ) as f:
            f.write(out)

        ret_value = get_avg( 'temp', run, runs, cpu, benchmark_verbose )

    return( ret_value )
############################################################################
def log(text = "", filename = None, encoding_txt = None):
    if filename is None:
        filename = 'test_results.txt'
    if encoding_txt is None:
        encoding_txt='utf_16_le'

    with open( filename, 'a', encoding=encoding_txt ) as f:
        print( text, file=f, flush=True )
############################################################################
def benchmark( saves, ticks, runs, benchmark_verbose = None, cpus = None, mod_directory = None ):
    if benchmark_verbose is None:
        benchmark_verbose = False
    if cpus is None:
        cpus = [0]
    if mod_directory is None:
        mod_directory = ""
    
    now = datetime.datetime.now()
    log( "----------------------" )
    for save in saves:
        if save != "":
            print('\nCurrent map = "{0}"'.format(save) )
            for cpu in cpus:
                ret_val = list()
                version = str()
                values = list()
                verbose_data = list()
                for i in range(1,runs+1):
                    ret_val = do_one_benchmark( save, ticks, i, 1, cpu, mod_directory, benchmark_verbose )
                    if len(ret_val) == 4:
                        version = ret_val[0]
                        values += ret_val[1]
                        if benchmark_verbose:
                            if len(verbose_data) < len(ret_val[3]):
                                verbose_data = ret_val[3]
                            else:
                                verbose_data = list( map(sum, zip(verbose_data, ret_val[3])) )

                if len( values ) > 0:
                    avg_ms = statistics.fmean( values )
                    min_ms = min( values )
                    pstdev = statistics.pstdev(values)
                else:
                    avg_ms = 999.0
                    min_ms = 999.0
                    pstdev = 0.0
                
                print('   avg = {0:.3f} ms  {1:.2f} FPS'.format(avg_ms, 1000.0/avg_ms) )
                print('   min = {0:.3f} ms  {1:.2f} FPS'.format(min_ms, 1000.0/min_ms) )

                log( '{} {:64} {:3}x{:8} ticks avg: {:10.3f} ms {:8.3f} FPS   {} {} {} pstdev={:.3f}{}'.format(now.strftime("%Y-%m-%d %H:%M"),save,runs,ticks,avg_ms,1000.0/avg_ms,version,platform.system(),get_cpu_str(cpu),pstdev,values ) )
                if benchmark_verbose:
                    log( ';'.join(str(x) for x in ret_val[2]) ) #columns
                    log( ';'.join("{0:.3f}".format(x/runs) for x in verbose_data) )
############################################################################

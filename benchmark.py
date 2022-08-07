import re
import platform
from enum import Enum

import datetime
import shutil
import statistics
import subprocess


############################################################################
def get_cpu_str( cpu = 0 ):
    if cpu == 0:
        return 'CPUxALL'
    else:
        return 'CPUx{0:02} '.format(cpu)
############################################################################
def get_avg(file_name, run = 1, runs = 1, cpu = 0, benchmark_verbose = False):
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
                print('run - {0}\t{1}\t{2:.2f} FPS\t{3}'.format(run, execution_time, 1000/a, get_cpu_str(cpu)))
                if len(avg) < runs:
                    step = Steps.EXECUTION_TIME_SEARCH
                else:
                    step = Steps.RUN1_SEARCH
        elif step == Steps.RUN1_SEARCH:
            if benchmark_verbose == False:
                break
            #
            # TODO: write code 'benchmark-verbose'
            #

    return( [version, avg] )
############################################################################
def do_one_benchmark( save, ticks = 1000, run = 1, runs = 1, cpu = 0, mod_directory = "", benchmark_verbose = False ):
    ret_value = list()

    if mod_directory == "":
        mod_directory = "temp_for_mod"
        try:
            shutil.rmtree( mod_directory )
        except OSError as e:
            pass
    argList = 'factorio.exe --mod-directory "{3}" --benchmark "{0}" --benchmark-ticks {1} --benchmark-runs {2} --disable-audio'.format(save, ticks, runs, mod_directory)
    if benchmark_verbose:
        argList = argList + ' --benchmark-verbose "all"'
    affinity_mask = 2**cpu - 1 #Windows https://docs.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-setprocessaffinitymask
    # start_factorio.exe:
    #   sets the process (factorio.exe) priority to HIGH
    #   sets the affinity for the process
    #   the output redirects to a file "temp"
    process = subprocess.run(['start_factorio.exe', argList, str( affinity_mask )], stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8', shell=True)
    if process.returncode != 0:
        # Error
        print( process.stdout )
        print( process.stderr )
    else:
        ret_value = get_avg( 'temp', run, runs, cpu, benchmark_verbose )

    return( ret_value )
############################################################################
def log(text = "", filename = 'test_results.txt', encoding_txt='utf_16_le'):
    with open( filename, 'a', encoding=encoding_txt ) as f:
        print( text, file=f, flush=True )
############################################################################
def benchmark( saves = [""], ticks = 1000, runs = 3, benchmark_verbose = False, cpus = [0], mod_directory = "" ):
    now = datetime.datetime.now()

    log( "----------------------" )
    for save in saves:
        if save != "":
            print('\nCurrent map = "{0}"'.format(save) )
            for cpu in cpus:
                ret_val = list()
                version = str()
                values = list()
                for i in range(1,runs+1):
                    ret_val = do_one_benchmark( save, ticks, i, 1, cpu, mod_directory, benchmark_verbose )
                    if len(ret_val) > 1:
                        version = ret_val[0]
                        values += ret_val[1]

                avg_ms = statistics.fmean( values )
                min_ms = min( values )
                
                print('   avg = {0:.3f} ms  {1:.2f} FPS'.format(avg_ms, 1000.0/avg_ms) )
                print('   min = {0:.3f} ms  {1:.2f} FPS'.format(min_ms, 1000.0/min_ms) )

                log( '{} {:64} {:3}x{:8} ticks avg: {:10.3f} ms {:8.3f} FPS   {} {} {} pstdev={:.3f}{}'.format(now.strftime("%Y-%m-%d %H:%M"),save,runs,ticks,avg_ms,1000.0/avg_ms,version,platform.system(),get_cpu_str(cpu),statistics.pstdev(values),values ) )
                    
############################################################################

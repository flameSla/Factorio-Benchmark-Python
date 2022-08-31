import datetime
from enum import Enum
import platform
import psutil
import re
import shutil
import statistics
import subprocess


############################################################################
def get_cpu_str(cpu):
    if cpu == 0:
        return 'CPUxALL'
    else:
        return 'CPUx{0:02} '.format(cpu)


############################################################################
def get_avg(file_name, run, runs, cpu, benchmark_verbose):

    class Steps(Enum):
        VERSION_SEARCH = 1
        EXECUTION_TIME_SEARCH = 2
        AVG_SEARCH = 3
        RUN1_SEARCH = 4
        GET_COLUMNS = 5
        GET_VALUES = 6

    ret_val = {'version': '',
               'list_avgs': list(),
               'column_names': list(),
               'verbose_averaged_values': list()}

    execution_time = ""
    step = Steps.VERSION_SEARCH
    tick = 0
    with open(file_name) as f:
        for line in f.readlines():
            line = line.rstrip()
            if step == Steps.VERSION_SEARCH:
                result = re.search(r'; Factorio (\d+\.\d+\.\d+)', line)
                if result:
                    ret_val['version'] = result[1]
                    step = Steps.EXECUTION_TIME_SEARCH
            elif step == Steps.EXECUTION_TIME_SEARCH:
                result = re.match(r'\s*Performed (\d*) updates in (\d*.\d* ms)', line)
                if result and result.lastindex == 2:
                    execution_time = result[2]
                    step = Steps.AVG_SEARCH
            elif step == Steps.AVG_SEARCH:
                result = re.match(r'\s*avg: (\d*.\d*) ms,', line)
                if result:
                    ret_val['list_avgs'].append(float(result[1]))
                    print('run - {0}\t\t{1}\t{2:.2f} FPS\t{3}'.format(run, execution_time, 1000/ret_val['list_avgs'][-1], get_cpu_str(cpu)))
                    if len(ret_val['list_avgs']) < runs:
                        step = Steps.EXECUTION_TIME_SEARCH
                    else:
                        if benchmark_verbose is True:
                            step = Steps.RUN1_SEARCH
                        else:
                            break
            elif step == Steps.RUN1_SEARCH:
                if line == 'run 1:':
                    step = Steps.GET_COLUMNS
            elif step == Steps.GET_COLUMNS:
                ret_val['column_names'] = line[0:-1].split(',')
                step = Steps.GET_VALUES
            elif step == Steps.GET_VALUES:
                if line[0] == 't':  # 't100, ...'
                    vals = [float(i)/1000000.0 for i in line[1:-1].split(',')]
                    tick = int(vals[0] * 1000000.0)
                    if not ret_val['verbose_averaged_values']:
                        ret_val['verbose_averaged_values'] = vals
                    else:
                        # calculating the sum of all values
                        ret_val['verbose_averaged_values'] = list(map(lambda a, b: a + b, ret_val['verbose_averaged_values'], vals))
                else:
                    tick += 1
                    print(tick)
                    # averaging
                    ret_val['verbose_averaged_values'] = [i/tick for i in ret_val['verbose_averaged_values']]
                    break

    return ret_val


############################################################################
def do_one_benchmark(save, ticks, run, runs, cpu, mod_directory, benchmark_verbose):
    ret_value = dict()

    if mod_directory == "":
        mod_directory = "temp_for_mod"
        try:
            shutil.rmtree(mod_directory)
        except OSError:
            pass

    argList = list()
    if platform.system() == 'Windows':
        argList.append('factorio.exe')
    elif platform.system() == 'Linux':
        argList.append('./factorio')

    argList.extend(['--mod-directory', mod_directory])
    argList.extend(['--benchmark', save])
    argList.extend(['--benchmark-ticks', str(ticks)])
    argList.extend(['--benchmark-runs', str(runs)])
    argList.append('--disable-audio')
    if benchmark_verbose:
        argList.extend(['--benchmark-verbose', 'all'])

    process = psutil.Popen(args=argList, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if platform.system() == 'Windows':
        process.nice(psutil.HIGH_PRIORITY_CLASS)
    elif platform.system() == 'Linux':
        process.nice(-20)

    if cpu != 0:
        process.cpu_affinity(list(range(0, cpu)))

    out, err = process.communicate()
    if process.returncode != 0:
        # Error
        print(out.decode())
        print(err.decode())
    else:
        with open('temp', 'wb') as f:
            f.write(out)

        ret_value = get_avg('temp', run, runs, cpu, benchmark_verbose)

    return ret_value


############################################################################
def get_default_value(param, default):
    if param is None:
        return default
    else:
        return param


############################################################################
def log(text="", filename=None, encoding_txt=None):
    filename = get_default_value(filename, 'test_results.txt')
    encoding_txt = get_default_value(encoding_txt, 'utf_16_le')

    with open(filename, 'a', encoding=encoding_txt) as f:
        print(text, file=f, flush=True)


############################################################################
def benchmark(saves, ticks, runs, benchmark_verbose=None, cpus=None, mod_directory=None):
    benchmark_verbose = get_default_value(benchmark_verbose, False)
    cpus = get_default_value(cpus, [0])
    mod_directory = get_default_value(mod_directory, "")

    now = datetime.datetime.now()
    log("----------------------")
    for save in saves:
        if save != "":
            print('\nCurrent map = "{0}"'.format(save))
            for cpu in cpus:
                version = str()
                avgs = list()
                verbose_data = list()
                ret_val = dict()
                for i in range(1, runs+1):
                    ret_val = do_one_benchmark(save, ticks, i, 1, cpu, mod_directory, benchmark_verbose)
                    if ret_val:
                        version = ret_val['version']
                        avgs.extend(ret_val['list_avgs'])
                        if benchmark_verbose:
                            if not verbose_data:
                                verbose_data = ret_val['verbose_averaged_values']
                            else:
                                verbose_data = list(map(lambda a, b: a + b, verbose_data, ret_val['verbose_averaged_values']))
                if avgs:
                    avg_ms = statistics.fmean(avgs)
                    min_ms = min(avgs)
                    pstdev = statistics.pstdev(avgs)
                else:
                    avg_ms = 999.0
                    min_ms = 999.0
                    pstdev = 0.0

                print('   avg = {0:.3f} ms  {1:.2f} FPS'.format(avg_ms, 1000.0/avg_ms))
                print('   min = {0:.3f} ms  {1:.2f} FPS'.format(min_ms, 1000.0/min_ms))

                log('{} {:64} {:3}x{:8} ticks avg: {:10.3f} ms {:8.3f} FPS   {} {} {} pstdev={:.3f}{}'.format(now.strftime("%Y-%m-%d %H:%M"), save, runs, ticks, avg_ms, 1000.0/avg_ms, version, platform.system(), get_cpu_str(cpu), pstdev, avgs))
                if benchmark_verbose and ret_val:
                    line = ';'.join("{0} = {1:.3f}".format(a, b/runs) for a, b in zip(ret_val['column_names'], ret_val['verbose_averaged_values']))
                    log(line)
############################################################################

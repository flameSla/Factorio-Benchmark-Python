from benchmark import benchmark

saves = list()
saves.append(r'template_for_benchmark')
# saves.append(r'')

ticks = 1000
runs = 3


# benchmark(saves, ticks, runs, benchmark_verbose, cpus=[0], mod_directory="")
benchmark(saves, ticks, runs, False, [2, 4, 8, 10, 0])
benchmark(saves, ticks, runs, True)

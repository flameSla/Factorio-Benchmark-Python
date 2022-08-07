## Factorio-Benchmark-Python

### Installing the script
Place files:

- benchmark.py
- template_for_benchmark.py
- template_for_benchmark.zip
- start_factorio.exe

next to factorio.exe

To check, run the script "template_for_benchmark.py"

### Usage:

1. Open the file "template_for_benchmark.py" in the editor.
2. Save the file with a different name.
3. Select saves for the benchmark:

replace the lines
```
saves.append( 'template_for_benchmark' )
#saves.append( '' )
```
with
```
saves.append( 'Test_fluids\\test_3k_100tiles_pipes_1000x' )
saves.append( 'Test_fluids\\test_3k_100tiles_pumps_1000x' )
saves.append( 'Test_fluids\\test_3k_100tiles_belts_1000x' )
```
4. Set ticks and runs
```
ticks = 1000
runs = 5
```
5. Set the verbose and cpus parameters
```
#benchmark( saves, ticks, runs, benchmark_verbose, cpus = [0], mod_directory = "" )
benchmark( saves, ticks, runs, False, [2,4,8,10,0] )
benchmark( saves, ticks, runs, True )
```
cpus - Allows you to limit the number of cores for factorio.exe
- [0] -> factorio.exe - uses all cores
- [2,4,0] -> 3 benchmarks will be made: 2 core limit, 4 core limit and no core limit

6. Save and run the script. The benchmark result will be saved to the file "test_results.txt".

import timeit
import benchmark


# line3 = '''t3,1946200,561500,0,560300,100,800,200,0,551600,0,100,0,0,0,0,0,0,0,0,0,0,100,200,300,0,100,0,200,0,700,100,200,'''
# line5 = '''t5,3071900,572000,0,571400,100,700,200,0,555700,0,0,0,0,0,0,0,0,0,0,0,0,100,400,400,0,100,0,200,0,100,100,100,'''
# a = line3[1:-1].split(',')
# print('a = ', a)
# print("for: ", min(timeit.repeat(lambda: [float(i)/1000000.0 for i in a], repeat=10)))
# print("map:", min(timeit.repeat(lambda: list(map(lambda i: float(i)/1000000.0, a)), repeat=10)))


print(benchmark.get_avg('test_temp', 1, 5, 0, True))
print(benchmark.do_one_benchmark("template_for_benchmark", 100, 1, 5, 0, "", True))

"""
{'version': '1.1.64',
 'list_avgs': [0.884, 0.821, 0.828, 0.823, 0.814],
 'column_names': ['tick', 'timestamp', 'wholeUpdate', 'latencyUpdate', 'gameUpdate', 'circuitNetworkUpdate', 'transportLinesUpdate', 'fluidsUpdate', 'heatManagerUpdate', 'entityUpdate', 'particleUpdate', 'mapGenerator', 'mapGeneratorBasicTilesSupportCompute', 'mapGeneratorBasicTilesSupportApply', 'mapGeneratorCorrectedTilesPrepare', 'mapGeneratorCorrectedTilesCompute', 'mapGeneratorCorrectedTilesApply', 'mapGeneratorVariations', 'mapGeneratorEntitiesPrepare', 'mapGeneratorEntitiesCompute', 'mapGeneratorEntitiesApply', 'crcComputation', 'electricNetworkUpdate', 'logisticManagerUpdate', 'constructionManagerUpdate', 'pathFinder', 'trains', 'trainPathFinder', 'commander', 'chartRefresh', 'luaGarbageIncremental', 'chartUpdate', 'scriptUpdate'],
 'verbose_averaged_values': [4.9500000000000004e-05, 48.767019, 0.8829790000000002, 0.0, 0.874801, 7.900000000000006e-05, 0.0015100000000000003, 0.00034300000000000037, 0.0, 0.8183059999999999, 0.0, 0.0001289999999999998, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0002660000000000004, 0.0003480000000000003, 0.0004110000000000004, 0.0, 0.00024300000000000002, 0.0, 0.0002779999999999998, 0.0, 0.006994999999999998, 0.00021799999999999977, 0.000263]}
""" 

import timeit


line = '''t3,1946200,561500,0,560300,100,800,200,0,551600,0,100,0,0,0,0,0,0,0,0,0,0,100,200,300,0,100,0,200,0,700,100,200,'''

a = line[1:-1].split(',')
print('a = ', a)
print("for: ", min(timeit.repeat(lambda: [float(i)/1000000.0 for i in a], repeat=10)))
print("map:", min(timeit.repeat(lambda: list(map(lambda i: float(i)/1000000.0, a)), repeat=10)))

print([float(i)/1000000.0 for i in line[1:-1].split(',')])
print(list(map(lambda i: float(i)/1000000.0, line[1:-1].split(','))))
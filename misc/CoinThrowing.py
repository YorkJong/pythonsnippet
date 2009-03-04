# Pythonic with space saving by ykjiang:
import random

N = 100
hist = (random.choice(('H', 'T')) for i in xrange(N))
m = {'H':0, 'T':0}
for e in hist:
    m[e] += 1
    print e
print 'H: ', m['H']
print 'T: ', m['T']


# Pythontic by ibmibm:
import random

N = 100
hist = [random.choice(('H', 'T')) for i in range(N)]
for e in hist:
    print e
print 'H:', hist.count('H')
print 'T:', hist.count('T')


# No Pythonic by timerover:
import random

N = 100
count = 0

for i in range(N):
    if random.randint(0, 1) == 1:
        count += 1
        print 'H'
    else:
        print 'T'

print 'H:', count
print 'T:', N - count

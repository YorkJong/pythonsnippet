"""
"""

def mod4(x,n):
    for i in xrange(n):
        yield x%4
        x /= 4


def decode(x,n):
    return "".join(["ATCG"[i] for i in mod4(x,n)])

# 4
def gen2(n):
    return [decode(x,n) for x in xrange(4**n)]


# 3. by zhouer
def gen0(n):
    if n == 0:
        return ['']
    else:
        return [x+y for x in ['A','T','C','G'] for y in gen0(n - 1)]


# 2
def gen0_1(n):
    if n == 0:
        return ['']
    else:
        return [x+y for x in gen0_1(n-1) for y in 'ATCG']

# 1
def gen0_2(n):
    I = list('ATCG')
    if n == 0:
        return ['']
    else:
        return [x+y for x in gen0_2(n-1) for y in I]


# by mantour
def gen1(n):
    L = ['']
    for i in range(n):
        tmp = [j+k for j in L for k in 'ATCG']
        L = tmp
    return L

# 2
def gen1_1(n):
    L = ['']
    for i in xrange(n):
        L = [j+k for j in L for k in 'ATCG']
    return L

# 1: most fast
def gen1_2(n):
    L = ['']
    I = list('ATCG')
    for i in xrange(n):
        L = [j+k for j in L for k in I]
    return L


import timeit
#print timeit.Timer("ATCG.gen(6)", "import ATCG").timeit(10)
#print timeit.Timer("ATCG.gen0(6)", "import ATCG").timeit(10)

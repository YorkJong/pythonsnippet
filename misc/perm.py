# -*- encoding: utf-8 -*-


def number_of_elements(n):
    """A decorator to fill n as second argument of a function.
    """
    def fill_n(f):
        def new_f(x):
            res = f(x, n)
            return res
        new_f.func_name = f.func_name
        return new_f
    return fill_n


def succN(x, n):
    """successor of x in the cycle of the permutation
    src: [0, 2, 4, 6, 8, 1, 3, 5, 7, 9]
    tgt: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    """
    if x%2 == 0:
        return x/2
    return n/2 + x/2


def predN(x, n):
    """predecessor of x in the cycle of the permutation
    src: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    tgt: [0, 2, 4, 6, 8, 1, 3, 5, 7, 9]
    """
    if x < n/2:
        return 2 * x
    return 2 * (x - n/2) + 1


def cycle_notation_from_one_line_notation(line):
    n = len(line)
    pred = line
    succ = dict(zip(line, range(n)))
    unmoved_set = set(range(n))
    cycles = []
    while unmoved_set:
        cycle = []
        s = unmoved_set.pop()
        x = succ[s]
        cycle.append(s)
        while x != s:
            unmoved_set.remove(x)
            cycle.append(x)
            x = succ[x]
        cycles.append(cycle)
    return cycles

    
def follow_cycles(p):
    """fllow-the-cycles algorithm for in-place permutations.
    for each length>1 cycle C of the permutation
        pick a starting address s in C
        let D = data at s
        let x = predecessor of s in the cycle
        while x ¡Ú s
            move data from x to successor of x
            let x = predecessor of x
        move data D to successor of s
    """
    n = len(p)
    succ = number_of_elements(n)(succN)
    pred = number_of_elements(n)(predN)
    unmoved_set = set(range(n))

    while unmoved_set:
        s = unmoved_set.pop()
        print 's:', s,
        d = p[s]
        x = pred(s)
        while x != s:
            p[succ(x)] = p[x]
            unmoved_set.remove(x)
            print 'x:', x,
            x = pred(x)
        p[succ(s)] = d
        print p

    return p

    
def test():
    p = range(10)
    n = len(p)
    succ = number_of_elements(n)(succN)
    pred = number_of_elements(n)(predN)
    ss = [succ(x) for x in p]
    print ss
    ps = [pred(x) for x in ss]
    print ps
    print
    p = follow_cycles(range(10))
    print
    print p
    print
    print cycle_notation_from_one_line_notation([0, 2, 4, 6, 8, 1, 3, 5, 7, 9])

"""
img[y][x]           # assuming this is the original orientation
i = y*w + x
x = i%w
y = i/w

img[x][w - y]       # rotated 90 degrees ccw
ii = x*w + (w-y) = (x + 1)*w - y

img[h - x][y]       # 90 degrees cw
ii = (h - x)*w + y

img[h - y][w - x]   # 180 degrees
ii = (h - y)*w + (w - x) = (h - y + 1) * w - x
"""

if __name__ == "__main__":
	test()
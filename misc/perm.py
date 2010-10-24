# -*- encoding: utf-8 -*-
"""
Permutation Operations

"""
__author__ = "Jiang Yu-Kuan, yukuan.jiang(at)gmail.com"
__date__ = "2006/10/25"
__revision__ = "1.1"


def cycle_notation_from_one_line_notation(line):
    """Return a cycle notation of a permutation from the corresponding one-line
    notation.

    Arguments
    ---------
    line
        a sequence to represent the one-line notation

    Reference
    ---------
    http://en.wikipedia.org/wiki/Permutation
    """
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

#------------------------------------------------------------------------------

def follow_cycles(seq, succ, pred):
    """Permute a sequence in place with follow-the-cycles algorithm.

    The follow-the-cycles algorithm::

        for each length>1 cycle C of the permutation
            pick a starting address s in C
            let D = data at s
            let x = predecessor of s in the cycle
            while x ¡Ú s
                move data from x to successor of x
                let x = predecessor of x
            move data D to successor of s

    Arguments
    ---------
    seq
        the sequence to be permuted
    succ
        a successor function
    pred
        a predecessor function

    Reference
    ---------
    http://en.wikipedia.org/wiki/Permutation

    """
    unmoved_set = set(range(len(seq)))

    while unmoved_set:
        s = unmoved_set.pop()
        d = seq[s]
        x = pred(s)
        while x != s:
            seq[succ(x)] = seq[x]
            unmoved_set.remove(x)
            x = pred(x)
        seq[succ(s)] = d

    return seq

#------------------------------------------------------------------------------

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


def succ_of_perm_even_odd(x, n):
    """Return successor of x in the cycle of a even-odd permutation.

    source: [0, 2, 4, 6, 8, 1, 3, 5, 7, 9]
    target: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    """
    if x%2 == 0:
        return x/2
    return n/2 + x/2


def pred_of_perm_even_odd(x, n):
    """Return predecessor of x in the cycle of a even-odd permutation.

    source: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    target: [0, 2, 4, 6, 8, 1, 3, 5, 7, 9]
    """
    if x < n/2:
        return 2 * x
    return 2 * (x - n/2) + 1

#------------------------------------------------------------------------------

def test():
    p = range(10)
    n = len(p)
    succ = number_of_elements(n)(succ_of_perm_even_odd)
    pred = number_of_elements(n)(pred_of_perm_even_odd)

    ss = [pred(x) for x in p]
    print ss
    ps = [succ(x) for x in ss]
    print ps

    print
    print cycle_notation_from_one_line_notation([0, 2, 4, 6, 8, 1, 3, 5, 7, 9])

    print follow_cycles(p, succ, pred)
    print p


if __name__ == "__main__":
	test()

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

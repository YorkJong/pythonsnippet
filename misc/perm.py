# -*- encoding: utf-8 -*-
"""
Operations of permutations in group theory

"""
__author__ = "Jiang Yu-Kuan, yukuan.jiang(at)gmail.com"
__date__ = "2006/10/25"
__revision__ = "1.1"

from functools import partial


#------------------------------------------------------------------------------
# Common Operations of Permutations
#------------------------------------------------------------------------------

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

    Example
    -------
    >>> cycle_notation_from_one_line_notation([0, 2, 4, 6, 8, 1, 3, 5, 7, 9])
    [[0], [1, 5, 7, 8, 4, 2], [3, 6], [9]]
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

def permute(seq, line):
    """Return a permuted sequence with a permutation in one-line notation

    Arguments
    ---------
    seq
        the sequence to be permuted
    line
        a permutation in one-line notation

    Example
    -------
    >>> seq = range(10)
    >>> permute(seq, [0, 2, 4, 6, 8, 1, 3, 5, 7, 9])
    [0, 2, 4, 6, 8, 1, 3, 5, 7, 9]
    """
    return [line[seq[x]] for x in range(len(seq))]


def permute_with_follow_cycles(seq, cycles):
    """Permute a sequence in place with a follow-the-cycles algorithm.

    Arguments
    ---------
    seq
        the sequence to be permuted
    cycles
        a permutation in cycle notation

    Reference
    ---------
    http://en.wikipedia.org/wiki/In-place_matrix_transposition

    Example
    -------
    >>> seq = range(10)
    >>> cycles = cycle_notation_from_one_line_notation([0, 2, 4, 6, 8, 1, 3, 5, 7, 9])
    >>> cycles
    [[0], [1, 5, 7, 8, 4, 2], [3, 6], [9]]
    >>> permute_with_follow_cycles(seq, cycles)
    >>> seq
    [0, 2, 4, 6, 8, 1, 3, 5, 7, 9]
    """
    def succ(cycle, x):
        n = len(cycle)
        dic = dict(zip(cycle, range(n)))
        return cycle[(dic[x] + 1) % n]

    def pred(cycle, x):
        n = len(cycle)
        dic = dict(zip(cycle, range(n)))
        return cycle[(dic[x] + n - 1) % n]

    for cycle in [c for c in cycles if len(c)>1]:
        s = cycle[0]
        d = seq[s]
        x = pred(cycle, s)
        while x != s:
            seq[succ(cycle, x)] = seq[x]
            x = pred(cycle, x)
        seq[succ(cycle, s)] = d


def permute_with_modified_follow_cycles(seq, succ, pred):
    """Permute a sequence in place with a modified follow-the-cycles algorithm.

    Arguments
    ---------
    seq
        the sequence to be permuted
    succ
        a successor function
    pred
        a predecessor function

    Example
    -------
    >>> seq = range(10)
    >>> n = len(seq)
    >>> succ = partial(succ_of_perm_even_odd, n=n)
    >>> pred = partial(pred_of_perm_even_odd, n=n)
    >>> permute_with_modified_follow_cycles(seq, succ, pred)
    >>> print seq
    [0, 2, 4, 6, 8, 1, 3, 5, 7, 9]
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

#------------------------------------------------------------------------------
# Apply Permutations to Even-odd bipartitions
#------------------------------------------------------------------------------

def succ_of_perm_even_odd(x, n):
    """Return successor of x in the cycle of a even-odd permutation.

    Example
    -------
    >>> seq = range(10)
    >>> succ = partial(succ_of_perm_even_odd, n=len(seq))
    >>> print [succ(x) for x in seq]
    [0, 5, 1, 6, 2, 7, 3, 8, 4, 9]
    """
    if x%2 == 0:
        return x/2
    return n/2 + x/2


def pred_of_perm_even_odd(x, n):
    """Return predecessor of x in the cycle of a even-odd permutation.

    Example
    -------
    >>> seq = range(10)
    >>> pred = partial(pred_of_perm_even_odd, n=len(seq))
    >>> print [pred(x) for x in seq]
    [0, 2, 4, 6, 8, 1, 3, 5, 7, 9]
    """
    if x < n/2:
        return 2 * x
    return 2 * (x - n/2) + 1

#------------------------------------------------------------------------------
# Apply Permutations to Picture Rotations
#------------------------------------------------------------------------------

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

#------------------------------------------------------------------------------
# Demonstration
#------------------------------------------------------------------------------

def demo():
    seq = range(10)
    print permute(seq, [0, 2, 4, 6, 8, 1, 3, 5, 7, 9])

    seq = range(10)
    cycles = cycle_notation_from_one_line_notation([0, 2, 4, 6, 8, 1, 3, 5, 7, 9])
    permute_with_follow_cycles(seq, cycles)
    print seq

    seq = range(10)
    n = len(seq)
    succ = partial(succ_of_perm_even_odd, n=n)
    pred = partial(pred_of_perm_even_odd, n=n)
    permute_with_modified_follow_cycles(seq, succ, pred)
    print seq


if __name__ == "__main__":
    import doctest
    failures, tests = doctest.testmod()
    if failures == 0:
        demo()


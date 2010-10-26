# -*- encoding: utf-8 -*-
"""
Operations of permutations in group theory

In group theory, the term permutation of a set means a bijective map, or
bijection, from that set onto itself.

References
----------
http://en.wikipedia.org/wiki/Permutation
http://en.wikipedia.org/wiki/Permutation_group
"""
__author__ = "Jiang Yu-Kuan, yukuan.jiang(at)gmail.com"
__date__ = "2006/10/25"
__revision__ = "1.2"

from functools import partial


#------------------------------------------------------------------------------
# Common Operations of Permutations
#------------------------------------------------------------------------------

def cycles_from_one_line(line):
    """Return a cycle notation of a permutation from the corresponding one-line
    notation.

    Arguments
    ---------
    line
        a sequence to denote a permutation in one-line notation.

    Note
    ----
    In group theory, there are three main notations for permutations of a finite
    set S: 1) two-line notation; 2) one-line notation; and 3) cycle notation.

    Reference
    ---------
    http://en.wikipedia.org/wiki/Permutation

    Example
    -------
    >>> one_line = [0, 2, 4, 6, 8, 1, 3, 5, 7, 9]   # even-odd bipartition
    >>> cycles_from_one_line(one_line)
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
    """Permute a sequence with a permutation in one-line notation.

    Arguments
    ---------
    seq
        the sequence to be permuted
    line
        a permutation in one-line notation

    Example
    -------
    >>> seq = range(10)
    >>> one_line = [0, 2, 4, 6, 8, 1, 3, 5, 7, 9]   # even-odd bipartition
    >>> permute(seq, one_line)
    [0, 2, 4, 6, 8, 1, 3, 5, 7, 9]
    """
    return [line[seq[x]] for x in range(len(seq))]


def permute_with_follow_cycles(seq, cycles):
    """Permute a sequence in place with a permutation in cycle notation.

    A follow-the-cycles algorithm is applied to this function.

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
    >>> one_line = [0, 2, 4, 6, 8, 1, 3, 5, 7, 9]   # even-odd bipartition
    >>> cycles = cycles_from_one_line(one_line)
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
    """Permute a sequence in place with successor and predecessor operations of
    a permutation.

    A modified follow-the-cycles algorithm is applied to this function.

    Arguments
    ---------
    seq
        the sequence to be permuted
    succ
        the successor function of a permutation
    pred
        the predecessor function of a permutation

    Example
    -------
    >>> seq = range(10)
    >>> n = len(seq)
    >>> succ = partial(succ_of_even_odd, n=n)
    >>> pred = partial(pred_of_even_odd, n=n)
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

def succ_of_even_odd(x, n):
    """Return successor of x in the cycle of a even-odd permutation.

    Example
    -------
    >>> seq = range(10)
    >>> succ = partial(succ_of_even_odd, n=len(seq))
    >>> print [succ(x) for x in seq]
    [0, 5, 1, 6, 2, 7, 3, 8, 4, 9]
    """
    if x%2 == 0:
        return x/2
    return n/2 + x/2


def pred_of_even_odd(x, n):
    """Return predecessor of x in the cycle of a even-odd permutation.

    Example
    -------
    >>> seq = range(10)
    >>> pred = partial(pred_of_even_odd, n=len(seq))
    >>> print [pred(x) for x in seq]
    [0, 2, 4, 6, 8, 1, 3, 5, 7, 9]
    """
    if x < n/2:
        return 2 * x
    return 2 * (x - n/2) + 1

#------------------------------------------------------------------------------
# Apply Permutations to Picture Rotations
#------------------------------------------------------------------------------

def succ_of_rotate90cw(i, w, h):
    """Return successor of i in the cycle of a permutation of rotation 90
    degree clockwise.
    """
    # w:h to h:w (rotate90cw)
    x = i%w
    y = i/w
    return x*h + (h-1)-y    # img[x][(h - 1) -  y]


def pred_of_rotate90cw(i, w, h):
    """Return predecessor of i in the cycle of a permutation of rotation 90
    degree clockwise.
    """
    # h:w to w:h (rotate90ccw)
    x = i%h
    y = i/h
    return (h-1 - x)*w + y  # img[(h - 1) - x][y]

#------------------------------------------------------------------------------

def succ_of_rotate90ccw(i, w, h):
    """Return successor of i in the cycle of a permutation of rotation 90
    degree counterclockwise.
    """
    pass

def pred_of_rotate90ccw(i, w, h):
    """Return predecessor of i in the cycle of a permutation of rotation 90
    degree counterclockwise.
    """
    pass

#------------------------------------------------------------------------------

def succ_of_rotate180(i, w, h):
    """Return successor of i in the cycle of a permutation of rotation 180
    degree.
    """
    pass


def pred_of_rotate180(i, w, h):
    """Return predecessor of i in the cycle of a permutation of rotation 180
    degree.
    """
    pass

#------------------------------------------------------------------------------
# Demonstration
#------------------------------------------------------------------------------

def demo():
    w, h = 4, 3
    seq = range(w*h)
    succ = partial(succ_of_rotate90cw, w=w, h=h)
    pred = partial(pred_of_rotate90cw, w=w, h=h)
    print seq
    print [succ(i) for i in seq]
    print [pred(i) for i in seq]


if __name__ == "__main__":
    import doctest
    failures, tests = doctest.testmod()
    if failures == 0:
        demo()


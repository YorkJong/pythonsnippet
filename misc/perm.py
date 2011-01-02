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
__date__ = "2010/10/25~2010/11/02"
__revision__ = "2.0"

from functools import partial


#------------------------------------------------------------------------------
# Help functions
#------------------------------------------------------------------------------

def gcd(a, b):
    """Return greatest common divisor using Euclid's Algorithm."""
    while b:
        a, b = b, a % b
    return a


def lcm(*args):
    """Return least common multiple of args."""
    return reduce(lambda a, b: a * b / gcd(a, b), args)

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


def one_line_from_cycles(cycles):
    """Return a one-line notation of a permutation from the corresponding cycle
    notation.

    Note
    ----
    In group theory, there are three main notations for permutations of a finite
    set S: 1) two-line notation; 2) one-line notation; and 3) cycle notation.

    Reference
    ---------
    http://en.wikipedia.org/wiki/Permutation

    Example
    -------
    >>> cycles = [[0], [1, 5, 7, 8, 4, 2], [3, 6], [9]] # even-odd bipartition
    >>> one_line_from_cycles(cycles)
    [0, 2, 4, 6, 8, 1, 3, 5, 7, 9]
    """
    pred = {}
    for c in cycles:
        n = len(c)
        pred.update((x, c[(i + n - 1) % n]) for i, x in enumerate(c))

    return [pred[x] for x in range(len(pred))]


def order_from_cycles(cycles):
    """Return the order of a cyclic permutation group.

    Arguments
    ---------
    cycles
        the cycle notation of a permutation

    Example
    -------
    >>> one_line = [0, 2, 4, 6, 8, 1, 3, 5, 7, 9]   # even-odd bipartition
    >>> cycles = cycles_from_one_line(one_line)
    >>> order_from_cycles(cycles)
    6
    """
    return lcm(*[len(c) for c in cycles])


def pred_in_cycle(cycle, x):
    """Return the predecessor of x in a cycle.

    Arguments
    ---------
    cycle
        the cycle represented by a sequence
    x
        the current element in the cycle

    Example
    -------
    >>> cycle = range(10)
    >>> pred_in_cycle(cycle, 1)
    0
    >>> pred_in_cycle(cycle, 0)
    9
    """
    n = len(cycle)
    dic = dict(zip(cycle, range(n)))
    return cycle[(dic[x] + n - 1) % n]


def succ_in_cycle(cycle, x):
    """Return the successor of x in a cycle.

    Arguments
    ---------
    cycle
        the cycle represented by a sequence
    x
        the current element in the cycle

    Example
    -------
    >>> cycle = range(10)
    >>> succ_in_cycle(cycle, 0)
    1
    >>> succ_in_cycle(cycle, 9)
    0
    """
    n = len(cycle)
    dic = dict(zip(cycle, range(n)))
    return cycle[(dic[x] + 1) % n]

#------------------------------------------------------------------------------
# Permute a sequence with different methods
#------------------------------------------------------------------------------

def permute_with_one_line(seq, line):
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
    >>> permute_with_one_line(seq, one_line)
    [0, 2, 4, 6, 8, 1, 3, 5, 7, 9]
    """
    return [line[seq[x]] for x in range(len(seq))]


def permute_with_cycles(seq, cycles):
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
    >>> permute_with_cycles(seq, cycles)
    >>> seq
    [0, 2, 4, 6, 8, 1, 3, 5, 7, 9]
    """
    for cycle in [c for c in cycles if len(c)>1]:
        s = cycle[0]
        d = seq[s]
        x = pred_in_cycle(cycle, s)
        while x != s:
            seq[succ_in_cycle(cycle, x)] = seq[x]
            x = pred_in_cycle(cycle, x)
        seq[succ_in_cycle(cycle, s)] = d


def permute_with_pred_and_succ(seq, pred, succ):
    """Permute a sequence in place with cycle operations of successor and
    predecessor for a permutation.

    A modified follow-the-cycles algorithm is applied to this function.

    Arguments
    ---------
    seq
        the sequence to be permuted
    pred
        the predecessor function of a permutation
    succ
        the successor function of a permutation

    Example
    -------
    >>> seq = range(10)
    >>> n = len(seq)
    >>> pred = partial(pred_of_even_odd, n=n)
    >>> succ = partial(succ_of_even_odd, n=n)
    >>> permute_with_pred_and_succ(seq, pred, succ)
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

#------------------------------------------------------------------------------
# Apply Permutations to Picture Rotations
#------------------------------------------------------------------------------

def pred_of_rotate90cw(i, w, h):
    """Return predecessor of i in the cycle of a permutation of rotation 90
    degree clockwise.

    Example
    -------
    >>> w, h = 4, 3
    >>> seq = range(w*h)
    >>> pred = partial(pred_of_rotate90cw, w=w, h=h)
    >>> [pred(i) for i in seq]
    [8, 4, 0, 9, 5, 1, 10, 6, 2, 11, 7, 3]
    """
    # h:w to w:h (rotate90ccw)
    x = i%h
    y = i/h
    return (h-1 - x)*w + y  # img[(h - 1) - x][y]


def succ_of_rotate90cw(i, w, h):
    """Return successor of i in the cycle of a permutation of rotation 90
    degree clockwise.

    Example
    -------
    >>> w, h = 4, 3
    >>> seq = range(w*h)
    >>> succ = partial(succ_of_rotate90cw, w=w, h=h)
    >>> [succ(i) for i in seq]
    [2, 5, 8, 11, 1, 4, 7, 10, 0, 3, 6, 9]
    """
    # w:h to h:w (rotate90cw)
    x = i%w
    y = i/w
    return x*h + (h-1)-y    # img[x][(h - 1) -  y]

#------------------------------------------------------------------------------

def pred_of_rotate90ccw(i, w, h):
    """Return predecessor of i in the cycle of a permutation of rotation 90
    degree counterclockwise.

    Example
    -------
    >>> w, h = 4, 3
    >>> seq = range(w*h)
    >>> pred = partial(pred_of_rotate90ccw, w=w, h=h)
    >>> [pred(i) for i in seq]
    [3, 7, 11, 2, 6, 10, 1, 5, 9, 0, 4, 8]
    """
    # h:w to w:h (rotate90cw)
    x = i%h
    y = i/h
    return x*w + (w-1)-y    # img[x][(w - 1) -  y]


def succ_of_rotate90ccw(i, w, h):
    """Return successor of i in the cycle of a permutation of rotation 90
    degree counterclockwise.

    Example
    -------
    >>> w, h = 4, 3
    >>> seq = range(w*h)
    >>> succ = partial(succ_of_rotate90ccw, w=w, h=h)
    >>> [succ(i) for i in seq]
    [9, 6, 3, 0, 10, 7, 4, 1, 11, 8, 5, 2]
    """
    # w:h to h:w (rotate90ccw)
    x = i%w
    y = i/w
    return (w-1 - x)*h + y  # img[(w - 1) - x][y]

#------------------------------------------------------------------------------

def pred_of_rotate180(i, w, h):
    """Return predecessor of i in the cycle of a permutation of rotation 180
    degree.

    Example
    -------
    >>> w, h = 4, 3
    >>> seq = range(w*h)
    >>> pred = partial(pred_of_rotate180, w=w, h=h)
    >>> [pred(i) for i in seq]
    [11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
    """
    # w:h to w:h (rotate180)
    x = i%w
    y = i/w
    return (h-1-y)*w + (w-1)-x  # img[(h - 1) - y][(w - 1) - x]


def succ_of_rotate180(i, w, h):
    """Return successor of i in the cycle of a permutation of rotation 180
    degree.
    """
    return pred_of_rotate180(i, w, h)

#------------------------------------------------------------------------------
# Demonstration
#------------------------------------------------------------------------------

def demo_rotate_cycles(w, h, pred_of_rotate=pred_of_rotate90cw):
    pred = partial(pred_of_rotate, w=w, h=h)

    seq = range(w*h)
    one_line = [pred(i) for i in seq]   # a permutation in one-line notation
    print '>>> one_line'
    print one_line
    cycles = cycles_from_one_line(one_line)
    print '>>> n of cycles'
    print len(cycles)
    print '>>> cycles'
    print cycles


def demo():
    w, h = 4, 3
    pred = partial(pred_of_rotate90cw, w=w, h=h)
    succ = partial(succ_of_rotate90cw, w=w, h=h)

    seq = range(w*h)
    one_line = [pred(i) for i in seq]   # a permutation in one-line notation
    print 'one_line:', one_line
    cycles = cycles_from_one_line(one_line)
    print 'cycles:', cycles
    order = order_from_cycles(cycles)
    print 'order:', order

    print '\nTest permute_with_one_line():'
    seq = range(w*h)
    for i in range(order):
        seq = permute_with_one_line(seq, one_line)
        print seq

    print '\nTest permute_with_cycles():'
    seq = range(w*h)
    for i in range(order):
        permute_with_cycles(seq, cycles)
        print seq

    print '\nTest permute_with_pred_and_succ():'
    seq = range(w*h)
    for i in range(order):
        permute_with_pred_and_succ(seq, pred, succ)
        print seq

    print '\ndemo_rotate_cycles with 3x4 blocks, 90CW:'
    demo_rotate_cycles(3, 4, pred_of_rotate90cw)

    print '\ndemo_rotate_cycles with 16x9 blocks, 90CW:'
    demo_rotate_cycles(16, 9, pred_of_rotate90cw)


if __name__ == "__main__":
    import doctest
    failures, tests = doctest.testmod()
    if failures == 0:
        demo()



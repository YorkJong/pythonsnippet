
def d0(seq, mod):
    a, b = 0, mod
    L = []
    while a<len(seq):
        L += [seq[a:b]]
        a += mod
        b += mod
        b = min(b, len(seq))
    return L


def seq_divide(seq, mod):
    """seq_divide(seq, mod) -> seq list
    >>> seq_divide('abcdefghijklmnopqr', 4)
    ['abcd', 'efgh', 'ijkl', 'mnop', 'qr']
    """
    A = range(0, len(seq), mod)
    B = A[1:] + [len(seq)]
    return [seq[a:b] for a, b in zip(A,B)]


def seq_divide1(seq, mod):
    """seq_divide1(seq, mod) -> seq list
    >>> seq_divide1('abcdefghijklmnopqr', 4)
    ['abcd', 'efgh', 'ijkl', 'mnop', 'qr']
    """
    return [seq[x:x+mod] for x in xrange(0, len(seq), mod)]


if __name__ == "__main__":
    print d0('abcdefghijklmnopqr', 4)
    print seq_divide('abcdefghijklmnopqr', 4)
    print seq_divide1('abcdefghijklmnopqr', 4)

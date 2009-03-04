"""
File: fract.py
"""
__author__ = "Jiang Yu-Kuan, yukuan.jiang(at)gmail.com"
__date__ = "2008/05/17"
__revision__ = "1.2"


def fract(x, bits=8, deduced=False):
    """Find p, q such that p/q ~= x and p<2**bits
    """
    p, q = x, 1
    while p < 2**bits:
        if deduced:
            print "%f = %d/%d" % (round(p)/float(q), round(p), q)
        p *= 2
        q *= 2
    return int(p/2+0.5), q/2


if __name__ == "__main__":
    p, q = fract(3.1415926535, deduced=True)
    print "p=%d, q=%d" % (p, q)

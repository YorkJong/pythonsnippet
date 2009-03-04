"""
Interactive random dot plotting.

This module demonstrates the usage of the interactive mode of matplotlib.
It is suggested to run this code under ipython. Details please see
http://matplotlib.sourceforge.net/interactive.html


Usage
=====

You can run this module in three ways:

    1. As a stand-alone application with GUI
    2. Run it on command line with a -d parameter to just generate the
       image with a specific format. (without GUI)
        * ref. http://matplotlib.sourceforge.net/backends.html
    3. Run it on ipython to call loop() many times

Examples
--------
You can simply run this module as a stand-alone application with GUI

    > irandot.py

Or just generate a image file with a specific format:

    > irandot.py -dAGG     # generate PNG file
    > irandot.py -dPS      # generate PS file
    > irandot.py -dSVG     # generate SVG file
    > irandot.py -dEMF     # generate EMF file

Running it with ipython is strongly suggested.

    In [1]: cd I:\trial\python  # suppose the module is put in I:\trial\python
    ...
    In [2]: run irandot.py
    ...
    In [3]: loop(50)
    ...
    In [4]: loop(20)
    ...

"""
__author__ = "Jiang Yu-Kuan, yukuan.jiang(at)gmail.com"
__date__ = "2006/09/24~2006/9/25"
__revision__ = "1.3"

from pylab import *


def dot_gen(dots=2):
    """A random dot generator.

    - dots: number of dots with plotting each loop
    """
    i = 0
    while 1:
        l, = plot(rand(dots), rand(dots), 'go')
        #setp(l, alpha=1,
        #    markerfacecolor='w', markeredgecolor='g', markersize=10)
        i += dots
        yield i


def loop(n=1):
    """Repeat dot plotting of n times."""
    g= dot_gen()  # gets a dot-plotting generator
    for i in xrange(n):
        print g.next(),


if __name__ == '__main__':
    if not isinteractive():
        ion()  # turns interactive on

    loop(50)
    savefig('irandot')

    try:
        __IPYTHON__
    except NameError:
        print "\nNOT on IPython"
        show()
    else:
        print "\nOn IPython"

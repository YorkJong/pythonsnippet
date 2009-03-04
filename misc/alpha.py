"""
Alpha band extractor
Reads .png files and generates corresponding .jpg files and alpha band hex
The alpha band means the 'A' band of 'RGBA' of pixels
"""
__author__ = "Jiang Yu-Kuan, yukuan.jiang(at)gmail.com"
__date__ = "2009/02/03~2009/02/13"
__version__ = "1.5"

import sys
import os
import glob
import getopt

from PIL import Image


def convert(infile, format):
    """Splits a PNG file into RGB part and alpha part.

    arguments:
    infile -- the input file name of the PNG image
    format -- the output file format of the RGB part
    """
    base, ext = os.path.splitext(infile)

    im = Image.open(infile)
    alpha = im.split()[3].getdata()
    hex_ = "".join(("%02X\n" % v for v in alpha))
    file(base+'.alpha.hex', 'wb').write(hex_)

    #im.save(base + '.jpg')  # progressive==progression (True==False==None bug??)
    im.convert('RGB').save(".".join([base, format]))

#------------------------------------------------------------------------------

def usage():
    print """\
Usage: alpha [option]

Option:
    -fEXT, --format=EXT assign RGB output format, e.g. JPG, BMP (the default).
    -h, --help          show this help message and exit.
    -v, --version       show version info. and exit.

Purpose:
    Read all RGBA .png files in current directory and split into Alpha part
    and RGB part."""


def main(args=None):
    if args is None:
        args = sys.argv[1:]
    else:
        args = args.split()
    try:
        opts, args = getopt.getopt(args, "hf:v",
                                   ["help", "format=", "version"])
    except getopt.GetoptError, err:
        print str(err)
        usage()
        return 2

    if args != []:
        usage()
        return 0

    format = 'bmp'
    for o, a in opts:
        if o in ("-f", "--format"):
            format = a
        elif o in ("-h", "--help"):
            usage()
            return 0
        elif o in ("-v", "--version"):
            print "PNG Alpha Extractor version",  __version__
            print "by ", __author__
            print __date__
            return 0
        else:
            assert False, "unhandled option"

    for infile in glob.glob('*.png'):
        print 'Processing', infile
        convert(infile, format.lower())


if __name__ == '__main__':
    sys.exit(main())


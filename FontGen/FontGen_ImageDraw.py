# -*- encoding: utf-8 -*-
"""
LCD Font Library Generator (PIL.ImageDraw version)
"""
__author__ = "Jiang Yu-Kuan <yukuan.jiang(at)gmail.com>"
__date__ = "2009/02/10~2009/02/15"
__version__ = "2.6"

import sys
import os
import re
from codecs import BOM_UTF16_LE, BOM_UTF16_BE, BOM_UTF8
from optparse import OptionParser, OptionValueError

from PIL import Image, ImageFont, ImageDraw

#-------------------------------------------------------------------------------

def RGB565_from_RGB888(rgb888, threshold):
    """Returns the RGB565 string from an RGB888 string

    arguments:
    rgb888 -- the input string
    threshold -- a unused dummy

    Example
    -------
    >>> RGB565_from_RGB888("\xf0"*3)
    '\xf7\x9e'
    """
    R = rgb888[0::3]
    G = rgb888[1::3]
    B = rgb888[2::3]
    R5 = (ord(r)>>(8-5)<<(6+5) for r in R)
    G6 = (ord(g)>>(8-6)<<5 for g in G)
    B5 = (ord(b)>>(8-5) for b in B)
    W = (r|g|b for r,g,b in zip(R5,G6,B5))
    return "".join((chr(w>>8)+chr(w&0xFF) for w in W))


def BW1_from_BW8(bw8, threshold):
    """Gets a BW1 string from a BW8 string.
    here BW1 means black-and-white 1-bit, 8 pixels per byte.
         BW8 means black-and-white 8-bit, 1 pixel per byte.

    arguments:
    bw8 -- the input string
    threshold -- the threshold for bileveling

    Example
    -------
    >>> BW1_from_BW8("\x00\xff"*6)
    'UP'
    """
    bytes = len(bw8)
    bw8 = (ord(b) for b in bw8)
    B = []
    b = 0x00
    m = 0x80
    for v in bw8:
        if v >= threshold:
            b |= m
        m >>= 1
        if m == 0x00:
            B.append(chr(b))
            b = 0x00
            m = 0x80
    if bytes%8 != 0:
        B.append(chr(b))
    return "".join(B)

#-------------------------------------------------------------------------------

def str_gen(mode, text, font, color, bgcolor):
    """Font generator with original string format.

    arguments:
    mode -- image mode must be "L" or "RGB"
    text -- characters of the font library
    font -- PIL.ImageFont
    bgcolor -- background color

    """
    assert mode in ("L", "RGB")
    w, h = get_fontsize(font)
    for char in text:
        im = Image.new(mode, (w, h), bgcolor)
        draw = ImageDraw.Draw(im)
        draw.text((0,0), char, font=font, fill=color)
        del draw
        yield im.tostring()


def lib_gen(mode, conv):
    """Font generator with final lib string format.

    arguments:
    mode -- image mode must be "L" or "RGB"
    conv -- convertor, e.g. RGB565_from_RGB888. BW1_from_BW8

    Example
    -------
    >>> font = load_font("cour.ttf", 12, "White")
    >>> mono_from_utf = lib_gen("L", BW1_from_BW8)
    >>> mono_from_utf("A", font, "Black", 164)
    '\x00\x00\x00\x80\x00\x00\x00\x00\x84\x00\x00\x00\x00'
    """
    def gen(text, font, color, bgcolor, threshold):
        S = []
        for s in str_gen(mode, text, font, color, bgcolor):
            S.append(conv(s, threshold))
        return "".join(S)
    return gen

#-------------------------------------------------------------------------------

def bilevel(s, threshold):
    im = Image.fromstring("L", (1, len(s)), s)
    im = im.point(lambda i: int(i >= threshold) * 255)
    return im.tostring()


def coord_gen(w, h, n, cols=16):
    y = -h
    for i in xrange(n):
        if i%cols == 0:
            x = 0
            y += h
        yield x, y, x+w, y+h    # start_x, start_y, end_x, end_y
        x += w


def preview(mode, text, font, color, bgcolor, threshold):
    w, h = get_fontsize(font)
    n = len(text)

    size = (w * min(16, n), h * (n + 8) / 16)
    im = Image.new(mode, size)

    shape = str_gen(mode, text, font, color, bgcolor)
    coord = coord_gen(w, h, n)
    for s, (x0, y0, x1, y1) in zip(shape, coord):
        if mode == "L": s = bilevel(s, threshold)
        im_char = Image.fromstring(mode, (w, h), s)
        im.paste(im_char, (x0, y0, x1, y1))

    im.show()

#-------------------------------------------------------------------------------

def get_fontsize(font):
    return font.getsize("W")


def select_font(filename, size):
    w0, h0 = size
    for i in xrange(30, 7, -1):
        font = ImageFont.truetype(filename, i)
        w, h = get_fontsize(font)
        if w<=w0 and h<=h0:
            break
    return w, h, font

#-------------------------------------------------------------------------------

def parse_opts(args):

    def check_color(option, opt_str, value, parser):
        pat = r"[a-fA-F0-9]{6}"    # "#rrggbb"
        if not re.match(pat, value):
            raise OptionValueError("Corlor format is #rrggbb")
        parser.values.__dict__[option.dest] = value

    usage = "usage: %prog [options] utf_file\n\t-h for help"
    version = "".join(["LCD Font Library Generator version ",  __version__,
                        "\nby ", __author__,
                        "\n", __date__])
    p = OptionParser(usage=usage, version=version)
    p.set_defaults(font="cour.ttf", size=(10, 20),
                   color="FFFFFF", bgcolor="000000",
                   type="RGB565", threshold=128, preview=False)

    p.add_option("-f", "--font", metavar="FILE",
                 help="set font file (default %(font)s)" % p.defaults)
    p.add_option("-s", "--size", nargs=2, metavar="m n", type="int",
                 help="set preferred font width and height"
                      " (default %(size)s)" % p.defaults)

    p.add_option("-c", "--color", metavar="RRGGBB", type="string",
                 action="callback", callback=check_color,
                 help="set font color (default %(color)s)" % p.defaults)
    p.add_option("-b", "--bgcolor", metavar="RRGGBB", type="string",
                 action="callback", callback=check_color,
                 help="set background color (default %(bgcolor)s)" % p.defaults)

    p.add_option("-t", "--type", metavar="TYPE (ex. RGB565, MONO)",
                 type="choice", choices=("RGB565", "MONO"),
                 help="set output type (default %(type)s)" % p.defaults)

    p.add_option("-T", "--threshold", metavar="n (0-255)", type="int",
                 help="set threshold (default %(threshold)d)"
                      " of MONO bileveling" % p.defaults)

    p.add_option("-p", "--preview", action="store_true",
                 help="preview the font on the screen")

    options, args = p.parse_args(args)

    if len(args) != 1 or not os.path.exists(args[0]):
        p.print_usage()
        sys.exit(3)

    options.color = "#" + options.color
    options.bgcolor = "#" + options.bgcolor
    if options.type == "MONO":
        options.color = "White"
        options.bgcolor = "Black"

    return options, args


def read_unicode(fn):
    inFile = open(fn, "rb")
    s = inFile.read()
    inFile.close()

    if s.startswith(BOM_UTF16_LE):
        u = s.decode("utf_16_le").lstrip(BOM_UTF16_LE.decode("utf_16_le"))
    elif s.startswith(BOM_UTF16_BE):
        u = s.decode("utf_16_be").lstrip(BOM_UTF16_BE.decode("utf_16_be"))
    else:
        u = s.decode("utf_8").lstrip(BOM_UTF8.decode("utf_8"))

    return u


def main(args=None):
    if args is None:
        args = sys.argv[1:]
    else:
        args = args.split()
    options, args = parse_opts(args)

    text = read_unicode(args[0])

    w, h, font = select_font(options.font, options.size)
    print "Actual font size:", w, h

    mode = {"RGB565": "RGB", "MONO": "L"}
    conv = {"RGB565": RGB565_from_RGB888, "MONO": BW1_from_BW8}

    gen = lib_gen(mode[options.type], conv[options.type])
    lib = gen(text, font, options.color, options.bgcolor, options.threshold)

    font_name = os.path.splitext(options.font)[0]
    lib_fn = font_name + "_w" + str(w) + "h" + str(h) \
             + "." + options.type + ".dat"

    print "Generating file:", lib_fn
    outfile = open(lib_fn, "wb")
    outfile.write(lib)
    outfile.close()

    if options.preview:
        preview(mode[options.type], text, font,
                options.color, options.bgcolor, options.threshold)


if __name__ == "__main__":
    sys.exit(main())

# -*- encoding: utf-8 -*-
"""
LCD Font Generator
"""
__author__ = "Jiang Yu-Kuan <yukuan.jiang(at)gmail.com>"
__date__ = "2009/02/10~2009/02/15"
__version__ = "1.5"

import sys
import os
import re
from optparse import OptionParser, OptionValueError

from PIL import Image, ImageDraw, ImageColor, ImageFont


#-------------------------------------------------------------------------------

def RGB565(im):
    """Return the RGB565 string from an Image object

    Example
    -------
    >>> im = Image.fromstring("RGB", (1,1), "\xf0"*3)
    >>> RGB565(im)
    '\xf7\x9e'
    """
    R, G, B = im.split()
    R, G, B = R.getdata(), G.getdata(), B.getdata()
    R5 = (r>>(8-5)<<(6+5) for r in R)
    G6 = (g>>(8-6)<<5 for g in G)
    B5 = (b>>(8-5) for b in B)
    W = (r|g|b for r,g,b in zip(R5,G6,B5))
    return "".join((chr(w>>8)+chr(w&0xFF) for w in W))


def RGB565s_from_utf(text, font, color="#FFFFFF", bgcolor="#000000"):
    size = font.getsize("W")
    S = []
    for char in text:
        im = Image.new("RGB", size, bgcolor)
        draw = ImageDraw.Draw( im )
        draw.text((0,0), char, font=font, fill=color)
        del draw
        S.append(RGB565(im))
    return "".join(S)

#-------------------------------------------------------------------------------

def mono(im):
    """Get an 1-bit bitmap string from an Image object

    Example
    -------
    >>> im = Image.fromstring("L", (3,4), "\x00\xff"*6)
    >>> mono(im)
    'UP'
    """
    color = ImageColor.getcolor("White", "L")
    data = im.convert("L").getdata()
    B = []
    b = 0x00
    m = 0x80
    for v in data:
        if v == color:
            b |= m
        m >>= 1
        if m == 0x00:
            B.append(b)
            b = 0x00
            m = 0x80
    if len(data)%8 != 0:
        B.append(b)
    return "".join((chr(v) for v in B))


def monos_from_utf(text, font):
    size = font.getsize("W")
    S = []
    for char in text:
        im = Image.new("1", size)
        draw = ImageDraw.Draw( im )
        draw.text((0,0), char, font=font, fill=1) # here 1 is "White"
        del draw
        S.append(mono(im))
    return "".join(S)

#-------------------------------------------------------------------------------

def preview(mode, text, font, color="#FFFFFF", bgcolor="#000000"):
    w, h = font.getsize("W")
    size = (w * min(16, len(text)), h * (len(text) + 8) / 16)
    im = Image.new(mode, size, bgcolor)
    draw = ImageDraw.Draw( im )
    y = -h
    for i, c in enumerate(text):
        if i%16 == 0:
            y += h
            x = 0
        draw.text((x, y), c, font=font, fill=color)
        x += w

    del draw
    im.show()

#-------------------------------------------------------------------------------

def parse_opts(args):

    def check_color(option, opt_str, value, parser):
        pat = r"[a-fA-F0-9]{6}"    # "#rrggbb"
        if not re.match(pat, value):
            raise OptionValueError("Corlor format is #rrggbb")
        parser.values.__dict__[option.dest] = value

    usage = "usage: %prog [options] utf_file\n\t-h for help"
    version = "".join(["LCD Font Generator version",  __version__,
                        "\nby ", __author__,
                        "\n", __date__])
    p = OptionParser(usage=usage, version=version)

    p.add_option("-f", "--font",
                 metavar="FILE",
                 help="set font file (default=cour.ttf)")
    p.add_option("-s", "--size", nargs=2,
                 metavar="M N", type="int",
                 help="set preferred font width and height (default=10 20)")

    p.add_option("-c", "--color", type="string",
                 metavar="RRGGBB", action="callback", callback=check_color,
                 help="set font color (default=FFFFFF)")
    p.add_option("-b", "--bgcolor", type="string",
                 metavar="RRGGBB", action="callback", callback=check_color,
                 help="set background color (default=000000)")

    p.add_option("-e", "--encode",
                 type="choice", choices=("utf8", "utf16"),
                 help="set encode of utf file, i.e., utf16 (default), or utf8")
    p.add_option("-t", "--type",
                 type="choice", choices=("RGB565", "MONO"),
                 help="set output type, i.e., RGB565 (default), or MONO")

    p.add_option("-p", "--preview",
                 action="store_true",
                 help="preview the font on the screen")

    p.set_defaults(font="cour.ttf", size=(10, 20),
                   color="FFFFFF", bgcolor="000000",
                   encode="utf16", type="RGB565", preview=False)

    options, args = p.parse_args(args)

    if len(args) != 1 or not os.path.exists(args[0]):
        p.print_usage()
        sys.exit(3)

    options.color = "#" + options.color
    options.bgcolor = "#" + options.bgcolor

    return options, args


def select_font(file, size):
    w0, h0 = size
    for i in xrange(30, 7, -1):
        font = ImageFont.truetype(file, size=i)
        w, h = font.getsize("W")
        if w<=w0 and h<=h0:
            break
    return w, h, font


def main(args=None):
    if args is None:
        args = sys.argv[1:]
    else:
        args = args.split()
    options, args = parse_opts(args)

    infile = open(args[0], "rb")
    text = infile.read().decode(options.encode)
    infile.close()

    w, h, font = select_font(options.font, options.size)
    print "Actual font size:", w, h
    if options.type == "RGB565":
        if options.preview:
            preview("RGB", text, font, options.color, options.bgcolor)
        out = RGB565s_from_utf(text, font, options.color, options.bgcolor)
    elif options.type == "MONO":
        if options.preview:
            preview("1", text, font)
        out = monos_from_utf(text, font)

    font_name, ext = os.path.splitext(options.font)
    out_fn = font_name + "_w" + str(w) + "h" + str(h) \
             + "." + options.type + ".dat"

    print "Generating file:", out_fn
    outfile = open(out_fn, "wb")
    outfile.write(out)
    outfile.close()


if __name__ == "__main__":
    sys.exit(main())

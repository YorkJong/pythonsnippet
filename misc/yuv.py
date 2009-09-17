
#------------------------------------------------------------------------------
# YPbPr
#------------------------------------------------------------------------------

def YPbPr(r, g, b, Kb=0.114, Kr=0.299):
    """Return YPbPr (analog version of Y'CbCr) from R'G'B'.

    Y' =  Kr * R'        + (1 - Kr - Kb) * G' + Kb * B'
    Pb = 0.5 * (B' - Y') / (1 - Kb)
    Pr = 0.5 * (R' - Y') / (1 - Kr)

    R', G', B' in [0, 1]
    Y' in [0, 1]
    Pb in [-0.5, 0.5]
    Pr in [-0.5, 0.5]

    ref. http://en.wikipedia.org/wiki/YCbCr
    """
    Y =  Kr * r + (1 - Kr - Kb) * g + Kb * b
    Pb = 0.5 * (b - Y) / (1 - Kb)
    Pr = 0.5 * (r - Y) / (1 - Kr)
    return Y, Pb, Pr

#------------------------------------------------------------------------------
# CCIR601
#------------------------------------------------------------------------------

def CCIR601(r, g, b):
    """Return CCIR-YCbCr (601) from RGB.

    CCIR 601 defines the relationship between YCbCr and RGB values:
        Ey = 0.299R + 0.587G + 0.114B
        Ecb = 0.564(B - Ey) = -0.169R - 0.331G + 0.500B
        Ecr = 0.713(R - Ey) =  0.500R - 0.419G - 0.081B

    where Ey, R, G and B are in the range [0, 1] and Ecr and Ecb are in the
    range [-0.5, 0.5].

    ref. http://www.fourcc.org/fccyvrgb.php
    """
    y = 0.299*r + 0.587*g + 0.114*b
    cb = (b-y)*0.564
    cr = (r-y)*0.713
    return y, cb, cr


def Rec601(r, g, b):
    """Return Rec-YCbCr (601-1) from RGB.

    CCIR Rec. 601-1 spec used by TIFF & JPEG (from David):
        Y  =  0.2989R + 0.5866G + 0.1145B         R = Y + 0.0000Cb + 1.4022Cr
        Cb = -0.1687R - 0.3312G + 0.5000B         G = Y - 0.3456Cb - 0.7145Cr
        Cr =  0.5000R - 0.4183G - 0.0816B         B = Y + 1.7710Cb + 0.0000Cr

    where R, G, B in [0, 255]; Y in [0, 255]; and Cb, Cr in [-128, 127]
    """
    y = 0.299*r + 0.587*g + 0.114*b
    cb = -0.1687*r - 0.3312*g + 0.5000*b
    cr = 0.5000*r - 0.4183*g - 0.0816*b
    return y, cb, cr


#------------------------------------------------------------------------------
# JFIF601
#------------------------------------------------------------------------------

def JFIF601(r, g, b):
    """Return JFIF-Y'CbCr (601) from "digital 8-bit R'G'B'"

    Y' =       + 0.299    * R'd + 0.587    * G'd + 0.114    * B'd
    Cb = 128   - 0.168736 * R'd - 0.331264 * G'd + 0.5      * B'd
    Cr = 128   + 0.5      * R'd - 0.418688 * G'd - 0.081312 * B'd

    R'd, G'd, B'd   in [0..255]
    Y', Cb, Cr      in [0..255]

    ref. http://en.wikipedia.org/wiki/YCbCr
    Note PIL use this.
    """
    y = 0.299 * r + 0.587 * g + 0.114 * b
    cb = 128 - 0.168736 * r - 0.331264 * g + 0.5 * b
    cr = 128 + 0.5 * r - 0.418688 * g - 0.081312 * b
    return y, cb, cr


def PIL(r, g, b):
    """Return PIL's JFIF-YCbCr (601) from 8-bit RGB.

    R, G, G in [0..255]
    Y, Cb, Cr in [0..255]
    """
    from PIL import Image
    im = Image.fromstring('RGB', (1,1), chr(r)+chr(g)+chr(b))
    return im.convert('YCbCr').getdata()[0]

#------------------------------------------------------------------------------
# Conversions
#------------------------------------------------------------------------------

def Clip(y, cb, cr):
    clip = lambda x: int((x + 256) % 256)
    y, cb, cr = clip(y), clip(cb), clip(cr)
    return y, cb, cr


def CCIR601FromJFIF601(y, cb, cr):
    return y, cb-128, cr-128

#------------------------------------------------------------------------------
# Chroma Subsampling
#------------------------------------------------------------------------------

def YUV444FromYUV422(YUV422):
    """Return the YUV444 string from a given YUV422 string

    An input byte stream with the order:
        Y0 U0 Y1 V1 Y2 U2 Y3 V3

    is reordered into:
        [Y0 U0 V1] [Y1 U0 V1] [Y2 U2 V3] [Y3 U2 V3]

    Example
    -------
    >>> YUV444FromYUV422('00112233YUYVYUYV')
    '001101223323YUVYUVYUVYUV'

    See Also
    --------
    http://en.wikipedia.org/wiki/Chroma_subsampling
    """
    Y = YUV422[::2]
    U = "".join((u*2 for u in YUV422[1::4]))
    V = "".join((v*2 for v in YUV422[3::4]))
    return "".join(y+u+v for y, u, v in zip(Y,U,V))


def YUV422FromYUV444(YUV444):
    """Return the YUV422 string from a given YUV444 string

    An input byte stream with the order:
        [Y0 U0 V0] [Y1 U1 V1] [Y2 U2 V2] [Y3 U3 V3]

    is reordered into:
        Y0 U0 Y1 V1 Y2 U2 Y3 V3

    Example
    -------
    >>> YUV422FromYUV444('000111222333YUVYUVYUVYUV')
    '00112233YUYVYUYV'

    See Also
    --------
    http://en.wikipedia.org/wiki/Chroma_subsampling
    """
    Y = YUV444[::3]
    U = YUV444[1::6]
    V = YUV444[5::6]
    UV = "".join((u+v for u, v in zip(U,V)))
    return "".join((y+uv for y, uv in zip(Y,UV)))

#------------------------------------------------------------------------------

def YUV444FromYUV411(YUV411):
    """Return the YUV444 string from a given YUV411 string

    An input byte stream with the order:
        Y0 U0 Y1 Y2 V2 Y3

    is reordered into:
        [Y0 U0 V2] [Y1 U0 V2] [Y2 U0 V2] [Y3 U0 V2]

    Example
    -------
    >>> YUV444FromYUV411('001223YUYYVY')
    '002102202302YUVYUVYUVYUV'

    See Also
    --------
    http://en.wikipedia.org/wiki/Chroma_subsampling
    """
    Y = "".join((y0+y1 for y0, y1 in zip(YUV411[::3], YUV411[2::3])))
    U = "".join((u*4 for u in YUV411[1::6]))
    V = "".join((v*4 for v in YUV411[4::6]))
    return "".join((y+u+v for y, u, v in zip(Y,U,V)))


def YUV411FromYUV444(YUV444):
    """Return the YUV411 string from a given YUV444 string

    An input byte stream with the order:
        [Y0 U0 V0] [Y1 U1 V1] [Y2 U2 V2] [Y3 U3 V3]

    is reordered into:
        Y0 U0 Y1 Y2 V2 Y3

    Example
    -------
    >>> YUV411FromYUV444('000111222333YUVYUVYUVYUV')
    '001223YUYYVY'

    See Also
    --------
    http://en.wikipedia.org/wiki/Chroma_subsampling
    """
    Y0 = YUV444[::12]
    Y1 = YUV444[3::12]
    Y2 = YUV444[6::12]
    Y3 = YUV444[9::12]
    U0 = YUV444[1::12]
    V2 = YUV444[8::12]
    return "".join(("".join([y0,u0,y1,y2,v2,y3])
                    for y0,u0,y1,y2,v2,y3 in zip(Y0,U0,Y1,Y2,V2,Y3)))

#------------------------------------------------------------------------------

def YUV444FromYUV420(YUV420, width):
    """Return the YUV444 string from a given YUV420 string

    An input byte stream with the order:
        Yo0 Uo0 Yo1 Yo2 Uo2 Yo3
        Ye0 Ve0 Ye1 Ye2 Ve2 Ye3

    is reordered into:
        [Yo0 Uo0 Ve0] [Yo1 Uo0 Ve0] [Yo2 Uo2 Ve2] [Yo3 Uo2 Ve2]
        [Ye0 Uo0 Ve0] [Ye1 Uo0 Ve0] [Ye2 Uo2 Ve2] [Ye3 Uo2 Ve2]

    Example
    -------
    >>> YUV444FromYUV420('001223001223ooooooeeeeeeYUYYUYYVYYVY', 4)
    '000100222322000100222322ooeooeooeooeeoeeoeeoeeoeYUVYUVYUVYUVYUVYUVYUVYUV'

    See Also
    --------
    http://en.wikipedia.org/wiki/Chroma_subsampling
    """
    from numpy import array, column_stack, hstack

    col = width*3/2
    row = len(YUV420)/col
    YUV420 = array(tuple(YUV420)).reshape((row,col))
    O420 = YUV420[0::2,:].flat
    E420 = YUV420[1::2,:].flat

    Yo = column_stack((O420[0::3], O420[2::3])).flat
    Ye = column_stack((E420[0::3], E420[2::3])).flat
    Uo0 = O420[1::6]
    Ve0 = E420[1::6]
    Uo2 = O420[4::6]
    Ve2 = E420[4::6]

    row /= 2
    col *= 2
    O444 = column_stack((Yo[0::4],Uo0,Ve0,Yo[1::4],Uo0,Ve0,
                         Yo[2::4],Uo2,Ve2,Yo[3::4],Uo2,Ve2)).reshape((row,col))
    E444 = column_stack((Ye[0::4],Uo0,Ve0,Ye[1::4],Uo0,Ve0,
                         Ye[2::4],Uo2,Ve2,Ye[3::4],Uo2,Ve2)).reshape((row,col))

    return "".join(hstack((O444, E444)).flat)


def YUV420FromYUV444(YUV444, width):
    """Return the YUV420 string from a given YUV444 string

    An input byte stream with the order:
        [Yo0 Uo0 Vo0] [Yo1 Uo1 Vo1] [Yo2 Uo2 Vo2] [Yo3 Uo3 Vo3]
        [Ye0 Ue0 Ve0] [Ye1 Ue1 Ve1] [Ye2 Ue2 Ve2] [Ye3 Ue3 Ve3]

    is reordered into:
        Yo0 Uo0 Yo1 Yo2 Uo2 Yo3
        Ye0 Ve0 Ye1 Ye2 Ve2 Ye3

    Example
    -------
    >>> s = '000111222333000111222333ooooooooooooeeeeeeeeeeeeYUVYUVYUVYUVYUVYUVYUVYUV'
    >>> YUV420FromYUV444(s, 4)
    '001223001223ooooooeeeeeeYUYYUYYVYYVY'

    See Also
    --------
    http://en.wikipedia.org/wiki/Chroma_subsampling
    """
    from numpy import array, column_stack, hstack

    col = width*3
    row = len(YUV444)/col
    YUV444 = array(tuple(YUV444)).reshape((row,col))
    O444 = YUV444[0::2,:].flat
    E444 = YUV444[1::2,:].flat

    Yo0 = O444[0::12]
    Yo1 = O444[3::12]
    Yo2 = O444[6::12]
    Yo3 = O444[9::12]
    Uo0 = O444[1::12]
    Uo2 = O444[7::12]
    Ye0 = E444[0::12]
    Ye1 = E444[3::12]
    Ye2 = E444[6::12]
    Ye3 = E444[9::12]
    Ve0 = E444[2::12]
    Ve2 = E444[8::12]

    row /= 2
    col /= 2
    O420 = column_stack((Yo0,Uo0,Yo1,Yo2,Uo2,Yo3)).reshape((row,col))
    E420 = column_stack((Ye0,Ve0,Ye1,Ye2,Ve2,Ye3)).reshape((row,col))

    return "".join(hstack((O420, E420)).flat)

#------------------------------------------------------------------------------
# Usage Example
#------------------------------------------------------------------------------

YUV = lambda r,g,b: Clip(*Rec601(r, g, b))


def demo():
    r, g, b = 0, 0, 255
    print JFIF601(r, g, b)
    print PIL(r, g, b)
    print
    print CCIR601FromJFIF601(*JFIF601(r, g, b))
    print CCIR601FromJFIF601(*PIL(r, g, b))
    print YPbPr(r, g, b)
    print CCIR601(r, g, b)
    print Rec601(r, g, b)
    print
    print Clip(*CCIR601FromJFIF601(*JFIF601(r, g, b)))
    print Clip(*CCIR601FromJFIF601(*PIL(r, g, b)))
    print Clip(*YPbPr(r, g, b))
    print Clip(*CCIR601(r, g, b))
    print Clip(*Rec601(r, g, b))


if __name__ == "__main__":
    import doctest
    failures, tests = doctest.testmod()
    if failures == 0:
        demo()

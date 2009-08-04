# -*- encoding: utf-8 -*-
"""
This tool generates char list with varied encodes
"""
__software__ = "Char Listing Tool"
__version__ = "1.0"
__author__ = "Jiang Yu-Kuan, yukuan.jiang(at)gmail.com"
__date__ = "2009/08/04 (initial version)"


def divide(sequence, modulus=32):
    """divide(sequence, modulus) -> sequence list
    >>> divide('abcdefghijklmnopqr', 4)
    ['abcd', 'efgh', 'ijkl', 'mnop', 'qr']
    """
    I = range(len(sequence))
    A = I[::modulus]
    B = A[1:] + [len(sequence)]
    return [sequence[a:b] for a, b in zip(A,B)]


Tbl = {
    'latin1':{
        'head':[
            '# ISO8859-1 (Latin-1)',
            '# ref. http://en.wikipedia.org/wiki/ISO/IEC_8859-1'
        ],
        'code':'iso8859-1',
        'range':((0x20,0x7F), (0xA0,0x0100))
    },
    'latin9':{
        'head':[
            '# ISO8859-15 (Latin-9)',
            '# ref. http://en.wikipedia.org/wiki/ISO/IEC_8859-15'
         ],
        'code':'iso8859-15',
        'range':((0x20,0x7F), (0xA0,0x0100))
    },
    'cp1252':{
        'head':[
            '# Windows-1252 (cp1252)',
            '# ref. http://en.wikipedia.org/wiki/Windows-1252'
         ],
        'code':'cp1252',
        'range':(
            (0x20,0x7F),
            (0x80,0x81), (0x82,0x8D), (0x8E,0x8F),
            (0x91,0x9D), (0x9E,0xA0),
            (0xA0,0x0100)
        )
    }
}


def gen_char_lst(name='latin1'):
    lines = Tbl[name]['head']
    for a, b in Tbl[name]['range']:
        lines.extend(['', ':0x%02X' % a])
        b = ''.join([chr(x) for x in range(a,b)])
        u = b.decode(Tbl[name]['code'])
        lines.extend(divide(u))

    fn = ''.join(['char_', name, '.lst'])
    f = open(fn, 'wb')
    f.write(u'\r\n'.join(lines).encode('utf16'))
    f.close()


if __name__ == '__main__':
    for name in Tbl.keys():
        gen_char_lst(name)

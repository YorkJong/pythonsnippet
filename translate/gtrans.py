# -*- encoding: utf-8 -*-
"""
A python wrapper of Google Translate web service.

This script is re-wrote from Thejaswi Raya's pytranslator for fitting my use.
For Thejaswi Raya's pytranslator, please see http://developer.spikesource.com \
/blogs/traya/2009/02/python_google_translator_pytra.html.
"""
__author__ = "Jiang Yu-Kuan, yukuan.jiang(at)gmail.com"
__date__ = "2009/03/03 (initial)"
__version__ = "1.0"

import sys
import re
import urllib


# from http://code.google.com/apis/ajaxlanguage/documentation/reference.html
_LANG_CODE = {
    'AFRIKAANS' : 'af',
    'ALBANIAN' : 'sq',
    'AMHARIC' : 'am',
    'ARABIC' : 'ar',
    'ARMENIAN' : 'hy',
    'AZERBAIJANI' : 'az',
    'BASQUE' : 'eu',
    'BELARUSIAN' : 'be',
    'BENGALI' : 'bn',
    'BIHARI' : 'bh',
    'BULGARIAN' : 'bg',
    'BURMESE' : 'my',
    'CATALAN' : 'ca',
    'CHEROKEE' : 'chr',
    'CHINESE' : 'zh',
    'CHINESE_SIMPLIFIED' : 'zh-CN',
    'CHINESE_TRADITIONAL' : 'zh-TW',
    'CROATIAN' : 'hr',
    'CZECH' : 'cs',
    'DANISH' : 'da',
    'DHIVEHI' : 'dv',
    'DUTCH': 'nl',
    'ENGLISH' : 'en',
    'ESPERANTO' : 'eo',
    'ESTONIAN' : 'et',
    'FILIPINO' : 'tl',
    'FINNISH' : 'fi',
    'FRENCH' : 'fr',
    'GALICIAN' : 'gl',
    'GEORGIAN' : 'ka',
    'GERMAN' : 'de',
    'GREEK' : 'el',
    'GUARANI' : 'gn',
    'GUJARATI' : 'gu',
    'HEBREW' : 'iw',
    'HINDI' : 'hi',
    'HUNGARIAN' : 'hu',
    'ICELANDIC' : 'is',
    'INDONESIAN' : 'id',
    'INUKTITUT' : 'iu',
    'ITALIAN' : 'it',
    'JAPANESE' : 'ja',
    'KANNADA' : 'kn',
    'KAZAKH' : 'kk',
    'KHMER' : 'km',
    'KOREAN' : 'ko',
    'KURDISH': 'ku',
    'KYRGYZ': 'ky',
    'LAOTHIAN': 'lo',
    'LATVIAN' : 'lv',
    'LITHUANIAN' : 'lt',
    'MACEDONIAN' : 'mk',
    'MALAY' : 'ms',
    'MALAYALAM' : 'ml',
    'MALTESE' : 'mt',
    'MARATHI' : 'mr',
    'MONGOLIAN' : 'mn',
    'NEPALI' : 'ne',
    'NORWEGIAN' : 'no',
    'ORIYA' : 'or',
    'PASHTO' : 'ps',
    'PERSIAN' : 'fa',
    'POLISH' : 'pl',
    'PORTUGUESE' : 'pt-PT',
    'PUNJABI' : 'pa',
    'ROMANIAN' : 'ro',
    'RUSSIAN' : 'ru',
    'SANSKRIT' : 'sa',
    'SERBIAN' : 'sr',
    'SINDHI' : 'sd',
    'SINHALESE' : 'si',
    'SLOVAK' : 'sk',
    'SLOVENIAN' : 'sl',
    'SPANISH' : 'es',
    'SWAHILI' : 'sw',
    'SWEDISH' : 'sv',
    'TAJIK' : 'tg',
    'TAIWAN' : 'zh-TW',
    'TAMIL' : 'ta',
    'TAGALOG' : 'tl',
    'TELUGU' : 'te',
    'THAI' : 'th',
    'TIBETAN' : 'bo',
    'TURKISH' : 'tr',
    'UKRAINIAN' : 'uk',
    'URDU' : 'ur',
    'UZBEK' : 'uz',
    'UIGHUR' : 'ug',
    'VIETNAMESE' : 'vi',
    'UNKNOWN' : ''
}


def lang_names():
    """
    Returns the name list of supported languages

    Example
    -------
    >>> 'Taiwan'.upper() in lang_names()
    True
    >>> 'Mars'.upper() in lang_names()
    False
    """
    return _LANG_CODE.keys()


def lang_codes():
    """
    Returns the code list of supported languages

    Example
    -------
    >>> 'zh-TW' in lang_codes()
    True
    """
    return _LANG_CODE.values()

#------------------------------------------------------------------------------
# Decorators
#------------------------------------------------------------------------------

def decor_name_to_code(func):
    """A decorator that converts arguments of language names
    into those of language codes."""
    def wrapper(text, src="English", dest="Taiwan"):
        names = lang_names()
        codes = lang_codes()

        if src.upper() in names:
            src = _LANG_CODE[src.upper()]
        if dest.upper() in names:
            dest = _LANG_CODE[dest.upper()]

        if src not in codes:
            src = "auto"
        if dest not in codes:
            dest = "auto"

        return func(text, src, dest)

    wrapper.__doc__ = func.__doc__
    wrapper.__name__ = func.__name__
    return wrapper


def decor_unicodify(func):
    """A decorator that converts unicode arguments into utf8 ones,
    and returns a unicode string."""
    def wrapper(*args):
        args_new = []
        for a in args:
            if isinstance(a, unicode):
                a = a.encode("utf8")
            args_new.append(a)

        return func(*args_new).decode("utf8")

    wrapper.__doc__ = func.__doc__
    wrapper.__name__ = func.__name__
    return wrapper

#------------------------------------------------------------------------------
# Public APIs
#------------------------------------------------------------------------------

@decor_name_to_code
@decor_unicodify
def translate(text, src="en", dest="zh-TW"):
    """Returns translated text for the given text supplied, matching the
    destination language.

    Arguments
    ---------
    text     - The text that is to be translated.
    src  - The source language as a language code
    dest - The destination language as a language code.

    Example
    -------
    >>> translate("你好世界", "auto", "English")
    u'Hello World'
    >>> translate("你好世界".decode("utf8"), "Taiwan", "English")
    u'Hello World'
    >>> translate("世界你好", "zh-TW", "en")
    u'Hello World'
    >>> translate("Bonjour Monde", "fr", "en")
    u'Hello World'
    >>> translate("ハローワールド", "ja", "en")
    u'Hello World'
    >>> translate("A bird can fly high.", "en", "fr")
    u'Un oiseau peut voler haut.'
    """
    URL_BASE = 'http://translate.google.com.tw/translate_t'

    params = {'langpair':'', 'text':'', 'ie':'UTF8', 'oe':'UTF8'}
    params['langpair'] = '%s|%s' % (src, dest)
    params['text'] = text

    urllib.FancyURLopener.version = "%s/%s" % (__file__, __version__)
    page = urllib.urlopen(URL_BASE, urllib.urlencode(params))
    content = page.read()
    page.close()

    match = re.search("<div id=result_box dir=\"ltr\">(.*?)</div>", content)
    return match.groups()[0]

#------------------------------------------------------------------------------
# Module Testing
#------------------------------------------------------------------------------

if __name__ == "__main__":
    import doctest
    failures, tests = doctest.testmod()
    if failures == 0:
        print translate("Pass the test.")

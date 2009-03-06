# -*- encoding: utf-8 -*-
"""
A wrapper of the AJAX Language API

ref. http://code.google.com/apis/ajaxlanguage
ref. http://code.google.com/p/python-googlelanguage/
"""
__author__ = "Jiang Yu-Kuan, yukuan.jiang(at)gmail.com"
__date__ = "2009/03/03 (initial)"
__version__ = "1.0"

import urllib

import simplejson


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
    Returns the name list of supported languages.

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
    Returns the code list of supported languages.

    Example
    -------
    >>> 'zh-TW' in lang_codes()
    True
    """
    return _LANG_CODE.values()

#------------------------------------------------------------------------------
# Decorators
#------------------------------------------------------------------------------

def name_to_code(func):
    """A decorator that converts arguments of language names
    into those of language codes.
    """
    def wrapper(text, src="English", dest="Taiwan"):
        names = lang_names()
        codes = lang_codes()

        if src.upper() in names:
            src = _LANG_CODE[src.upper()]
        if dest.upper() in names:
            dest = _LANG_CODE[dest.upper()]

        if src not in codes:
            src = detect(text).encode("utf8")
        if dest not in codes:
            dest = "en"

        return func(text, src, dest)

    wrapper.__doc__ = func.__doc__
    wrapper.__name__ = func.__name__
    return wrapper


def unicode_to_utf8(func):
    """A decorator that converts unicode arguments into utf8 ones."""
    def wrapper(*args):
        args_new = []
        for a in args:
            if isinstance(a, unicode):
                a = a.encode("utf8")
            args_new.append(a)

        return func(*args_new)

    wrapper.__doc__ = func.__doc__
    wrapper.__name__ = func.__name__
    return wrapper

#------------------------------------------------------------------------------
# Public APIs
#------------------------------------------------------------------------------

@name_to_code
@unicode_to_utf8
def translate(text, src="en", dest="zh-TW"):
    """Returns translated text for the given text supplied, matching the
    destination language.

    Arguments
    ---------
    text     - The text that is to be translated.
    src  - The source language
    dest - The destination language

    Example
    -------
    >>> translate("世界你好", "zh-TW", "en")
    u'Hello World'
    >>> translate("Bonjour Monde", u"fr", u"en")
    u'Hello World'
    >>> translate("ハローワールド", "Japanese", "en")
    u'Hello World'
    >>> translate(u"A bird can fly high.", "en", "fr")
    u'Un oiseau peut voler haut.'
    """
    URL_BASE = 'http://ajax.googleapis.com/ajax/services/language/translate'

    params = {'v':'1.0', 'q':'', 'langpair':''}
    params['q'] = text
    params['langpair'] = '%s|%s' % (src, dest)

    url = '%s?%s' % (URL_BASE, urllib.urlencode(params))
    fp = urllib.urlopen(url)
    json = fp.read()  # get the JSON string
    fp.close()

    json = simplejson.loads(json)  # parse the JSON string

    if json['responseStatus'] == 200:
        return json['responseData']['translatedText']
    else:
        raise Exception('(%(responseStatus)s) %(responseDetails)s' % json)

    return None


@unicode_to_utf8
def detect(text):
    """Return the language code that describes the language of the given text.

    Arguments
    ---------
    text - The text that is to be translated.

    Example
    -------
    >>> detect("Stand Alone Complex")
    u'en'
    >>> detect("將麵和面一起服下肚")
    u'zh-TW'
    >>> detect("面皮")
    u'zh-CN'
    """
    URL_BASE = 'http://ajax.googleapis.com/ajax/services/language/detect'

    params = {'v':'1.0', 'q':''}
    params['q'] = text

    url = '%s?%s' % (URL_BASE, urllib.urlencode(params))
    fp = urllib.urlopen(url)
    json = fp.read()  # get the JSON string
    fp.close()

    json = simplejson.loads(json)  # parse the JSON string

    if json['responseStatus'] == 200:
        return json['responseData']['language']
    else:
        raise Exception('(%(responseStatus)s) %(responseDetails)s' % json)

    return None

#------------------------------------------------------------------------------
# Module Testing
#------------------------------------------------------------------------------

if __name__ == "__main__":
    import doctest
    failures, tests = doctest.testmod()
    if failures == 0:
        print translate("Pass the test.")

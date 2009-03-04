# -*- encoding: utf-8 -*-
"""
A wrapper of the AJAX Language API

ref. http://code.google.com/p/python-googlelanguage/source/browse/trunk/googlelanguage/__init__.py
ref. http://code.google.com/apis/ajaxlanguage/documentation/reference.html#_intro_fonje
"""
__author__ = "Jiang Yu-Kuan, yukuan.jiang(at)gmail.com"
__date__ = "2009/03/03 (initial)"
__version__ = "1.0"

import urllib

import simplejson


# from http://code.google.com/apis/ajaxlanguage/documentation/reference.html#LangNameArray
_langCode = {
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

#------------------------------------------------------------------------------
# Decorators
#------------------------------------------------------------------------------

def _language_name(func):
    def wrapper(text, src, dest):
        """Supports language name for argument "src" and "dest"."""
        names = _langCode.keys()
        codes = _langCode.values()

        src, dest = src.upper(), dest.upper()
        if src in names:
            src = _langCode[src]
        if dest in names:
            dest = _langCode[dest]

        src, dest = src.lower(), dest.lower()
        if src not in codes:
            src = detect(text).encode("utf8")
        if dest not in codes:
            dest = "en"

        return func(text, src, dest)

    wrapper.__doc__ = func.__doc__
    wrapper.__name__ = func.__name__
    return wrapper


def _unicode_text(func):
    def wrapper(text, *args, **kwargs):
        """Supports unicode for argument "text"."""
        if isinstance(text, unicode):
            text = text.encode("utf8")

        return func(text, *args, **kwargs)

    wrapper.__doc__ = func.__doc__
    wrapper.__name__ = func.__name__
    return wrapper

#------------------------------------------------------------------------------
# Public APIs
#------------------------------------------------------------------------------

@_unicode_text
@_language_name
def translate(text, srcLang='en', destLang='zh-TW'):
    """Returns translated text for the given text supplied, matching the
    destination language.

    Arguments
    ---------
    text     - The text that is to be translated.
    srcLang  - The source language
    destLang - The destination language

    Example
    -------
    >>> translate("世界你好", "zh-TW", "en")
    u'Hello World'
    >>> translate("世界你好", "zh-TW", "fr")
    u'Bonjour tout le monde'
    >>> translate("Bonjour tout le monde", "fr", "en")
    u'Hello World'
    >>> translate("ハローワールド", "Japanese", "en")
    u'Hello World'
    >>> translate("A bird can fly high.", "en", "fr")
    u'Un oiseau peut voler haut.'
    """
    TRANSLATE_URL = 'http://ajax.googleapis.com/ajax/services/language/translate?'
    TRANSLATE_PARAMS = {'v':'1.0', 'q':'', 'langpair':''}

    params = TRANSLATE_PARAMS
    params['q'] = text
    params['langpair'] = '|'.join([srcLang, destLang])

    url = TRANSLATE_URL + urllib.urlencode(params)
    fp = urllib.urlopen(url)
    resp = fp.read()  # get the JSON string
    fp.close()

    resp = simplejson.loads(resp)  # parse the JSON string

    if resp['responseStatus'] == 200:
        return resp['responseData']['translatedText']
    else:
        raise Exception('(%(responseStatus)s) %(responseDetails)s' % resp)

    return None


@_unicode_text
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
    DETECT_URL = 'http://ajax.googleapis.com/ajax/services/language/detect?'
    DETECT_PARAMS = {'v':'1.0', 'q':''}

    params = DETECT_PARAMS
    params['q'] = text

    url = DETECT_URL + urllib.urlencode(params)
    fp = urllib.urlopen(url)
    resp = fp.read()  # get the JSON string
    fp.close()

    resp = simplejson.loads(resp)  # parse the JSON string

    if resp['responseStatus'] == 200:
        return resp['responseData']['language']
    else:
        raise Exception('(%(responseStatus)s) %(responseDetails)s' % resp)

    return None

#------------------------------------------------------------------------------
# Module Testing
#------------------------------------------------------------------------------

if __name__ == "__main__":
    import doctest
    doctest.testmod()

# -*- encoding: utf-8 -*-
"""
A python wrapper of the web service of Google Translate
"""
__author__ = "Jiang Yu-Kuan, yukuan.jiang(at)gmail.com"
__date__ = "2009/03/03 (initial)"
__version__ = "1.0"

import sys
import re
import urllib


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


def language_name(func):
    def wrapper(text, src, dest):
        lang_names = _langCode.keys()
        src, dest = src.upper(), dest.upper()

        if src in lang_names:
            src = _langCode.get(src, "auto")
        if dest in lang_names:
            dest = _langCode.get(dest, "auto")

        return func(text, src, dest)

    return wrapper


def unicode_text(func):
    def wrapper(text, *args, **kwargs):
        if isinstance(text, unicode):
            text = text.encode("utf8")

        return func(text, *args, **kwargs).decode("utf8")

    return wrapper


@unicode_text
@language_name
def translate(text, srcLang="en", destLang="zh-TW"):
    """Returns translated text for the given text supplied, matching the
    destination language.

    Arguments
    ---------
    text     - The text that is to be translated.
    srcLang  - The source language as a language code
    destLang - The destination language as a language code.

    Example
    -------
    >>> translate("你好世界", "auto", "English")
    u'Hello World'
    >>> translate("你好世界".decode("utf8"), "Taiwan", "English")
    u'Hello World'
    >>> translate("世界你好", "zh-TW", "en")
    u'Hello World'
    >>> translate("世界你好", "zh-TW", "fr")
    u'Bonjour tout le monde'
    >>> translate("Bonjour tout le monde", "fr", "en")
    u'Hello World'
    >>> translate("ハローワールド", "ja", "en")
    u'Hello World'
    >>> translate("A bird can fly high.", "en", "fr")
    u'Un oiseau peut voler haut.'

    See Also
    --------
    http://developer.spikesource.com/blogs/traya/2009/02/python_google_translator_pytra.html
    """
    urllib.FancyURLopener.version = "Firefox/3.0.6"

    params = urllib.urlencode({
        "langpair": "%(srcLang)s|%(destLang)s" % locals(),
        "text": text,
        "ie":"UTF8", "oe":"UTF8"
    })

    base = "http://translate.google.com.tw/translate_t"
    page = urllib.urlopen(base, params)
    content = page.read()
    page.close()

    match = re.search("<div id=result_box dir=\"ltr\">(.*?)</div>", content)
    value = match.groups()[0]
    return value


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print translate("你好世界", "auto", "English")
    print translate("你好世界".decode("utf8"), "Taiwan", "English")
    print translate("世界你好", "zh-TW", "en")

# -*- encoding: utf-8 -*-
"""
A wrapper of Google Translate
"""
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


def translate(text, srcLang="English", destLang="Taiwan"):
    """
    Returns a translated unicode string from a string.

    ref. http://developer.spikesource.com/blogs/traya/2009/02/python_google_translator_pytra.html
    """
    src = _langCode.get(srcLang.upper(), "auto")
    dest = _langCode.get(destLang.upper(), "auto")

    urllib.FancyURLopener.version = "Firefox/3.0.6"

    if isinstance(text, unicode):
        text = text.encode("utf8")

    params = urllib.urlencode({
        "langpair": "%(src)s|%(dest)s" % locals(),
        "text": text,
        "ie":"UTF8", "oe":"UTF8"
    })

    base = "http://translate.google.com.tw/translate_t"
    page = urllib.urlopen(base, params)
    content = page.read()
    page.close()

    match = re.search("<div id=result_box dir=\"ltr\">(.*?)</div>", content)
    value = match.groups()[0]
    return value.decode("utf8")


if __name__ == "__main__":
    print translate("Pass the test.")

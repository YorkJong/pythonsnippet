"""
A wrapper of the AJAX Language API

ref. http://code.google.com/p/python-googlelanguage/source/browse/trunk/googlelanguage/__init__.py
ref. http://code.google.com/apis/ajaxlanguage/documentation/reference.html#_intro_fonje
"""

import urllib, simplejson


def translate(text, srcLang='en', destLang='zh-TW'):
    """Returns translated text for the given text supplied, matching the
    destination language.

    Arguments
    ---------
    text     - The text that is to be translated.
    srcLang  - The source language as a language code
    destLang - The destination language as a language code.
    ---------

    """
    TRANSLATE_URL = 'http://ajax.googleapis.com/ajax/services/language/translate?'
    TRANSLATE_PARAMS = {'v':'1.0', 'q':'', 'langpair': ''}

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


def detect(text):
    """Return the language code that describes the language of the given text.

    Arguments
    ---------
    text - The text that is to be translated.


    Example
    -------
    >>> detect("What the language.")
    u'en'
    """
    DETECT_URL = 'http://ajax.googleapis.com/ajax/services/language/detect?'
    DETECT_PARAMS = {'v':'1.0', 'q':'', }

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


if __name__ == "__main__":
    print translate("Pass the test.")
    #import doctest
    #doctest.testmod()

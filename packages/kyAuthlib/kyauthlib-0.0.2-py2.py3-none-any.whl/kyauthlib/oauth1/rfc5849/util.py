from kyauthlib.common.urls import quote
from kyauthlib.common.urls import unquote


def escape(s):
    return quote(s, safe=b"~")


def unescape(s):
    return unquote(s)

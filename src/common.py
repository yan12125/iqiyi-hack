import os.path

try:
    import urllib.request as compat_urllib_request
except ImportError:
    import urllib2 as compat_urllib_request

try:
    import urllib.parse as compat_urlparse
except ImportError:
    import urlparse as compat_urlparse

try:
    import http.server as compat_http_server
except ImportError:
    import BaseHTTPServer as compat_http_server

compat_urllib_request
compat_urlparse
compat_http_server

ROOT = os.path.dirname(os.path.abspath(__file__))


def full_path(p):
    return os.path.join(ROOT, p)

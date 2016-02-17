import re

try:
    from urllib.request import urlopen as compat_urllib_request_urlopen
except ImportError:
    from urllib2 import urlopen as compat_urllib_request_urlopen

PAGE_URL = 'http://www.iqiyi.com/v_19rrojlavg.html'
DOMAIN = 'www.iqiyi.com'
PATCH_FILENAME = 'iqiyi.patch'


def get_site_swf():
    print('Downloading the page %s' % PAGE_URL)
    urlh = compat_urllib_request_urlopen(PAGE_URL)
    webpage = urlh.read().decode('utf-8')
    urlh.close()
    mobj = re.search(r'http://[^\'"]+MainPlayer[^.]+\.swf', webpage)
    swf_url = mobj.group(0)

    print('SWF URL is %s' % swf_url)

    return swf_url

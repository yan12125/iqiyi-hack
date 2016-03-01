import re

from common import compat_urllib_request

PAGE_URL = 'http://www.iqiyi.com/v_19rrojlavg.html'
DOMAIN = 'www.iqiyi.com'
PATCH_FILENAME = 'iqiyi.patch'


def get_site_swf():
    print('Downloading the page %s' % PAGE_URL)
    urlh = compat_urllib_request.urlopen(PAGE_URL)
    webpage = urlh.read().decode('utf-8')
    urlh.close()
    mobj = re.search(
        r'data-flashplayerparam-flashurl="(http://[^"]+.swf)"',
        webpage)
    swf_url = mobj.group(1)

    print('SWF URL is %s' % swf_url)

    return swf_url

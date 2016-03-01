import re

from common import compat_urllib_request

PAGE_URL = 'http://www.douyutv.com/iseven'
DOMAIN = 'www.douyutv.com'
PATCH_FILENAME = 'douyu.patch'


def get_site_swf():
    HOME_URL = 'http://www.douyutv.com/'
    print('Downloading the page %s' % HOME_URL)
    urlh = compat_urllib_request.urlopen(HOME_URL)
    webpage = b''
    while True:
        webpage += urlh.read(1024)
        mobj = re.search(br'"swf_ver":"([^"]+)"', webpage)
        if mobj:
            break
    swf_ver = mobj.group(1).decode('utf-8')
    swf_url = 'http://staticlive.douyutv.com/common/simplayer/core.swf?' + swf_ver

    print('SWF URL is %s' % swf_url)

    return swf_url


KEY = b"dkrltl0%4*@jrky#@$"


def decrypt_swf(data):
    output = []
    for i in range(0, 50):
        for a, b in zip(data[i * len(KEY):(i + 1) * len(KEY)], KEY):
            output.append((a - b) % 256)
    output += data[len(KEY) * 50:]

    return bytearray(output)


def encrypt_swf(data):
    output = []
    for i in range(0, 50):
        for a, b in zip(data[i * len(KEY):(i + 1) * len(KEY)], KEY):
            output.append((a + b) % 256)
    output += data[len(KEY) * 50:]

    return bytearray(output)

if __name__ == '__main__':
    with open('src/core.swf?v26710', 'rb') as f:
        data = decrypt_swf(f.read())

    with open('src/core2.swf', 'wb') as f:
        f.write(data)

import errno
import os
import os.path
import re
import shutil
import subprocess
import threading
try:
    from urllib.request import urlopen as compat_urllib_request_urlopen
except ImportError:
    from urllib2 import urlopen as compat_urllib_request_urlopen

try:
    from urllib.request import urlretrieve as compat_urllib_request_urlretrieve
except ImportError:
    from urllib import urlretrieve as compat_urllib_request_urlretrieve

from config import PAGE_URL
from server import run_server
from selenium_runner import SeleniumRunner
from common import full_path


def get_swf():
    print('Downloading the page %s' % PAGE_URL)
    urlh = compat_urllib_request_urlopen(PAGE_URL)
    webpage = urlh.read().decode('utf-8')
    urlh.close()
    mobj = re.search(r'http://[^\'"]+MainPlayer[^.]+\.swf', webpage)
    swf_url = mobj.group(0)
    swf_path = full_path(os.path.basename(swf_url))

    print('SWF URL is %s' % swf_url)

    compat_urllib_request_urlretrieve(swf_url, filename=swf_path)
    return swf_path, swf_url


def run(args):
    print(' '.join(args))
    subprocess.check_call(args)


def patch_swf(swf_path):
    swf_name = os.path.splitext(os.path.basename(swf_path))[0]
    abc_index = 0
    abc_id = '%s-%d' % (swf_name, abc_index)

    try:
        os.remove(full_path('%s.abc' % abc_id))
        shutil.rmtree(full_path(abc_id))
    except OSError as e:
        if e.errno != errno.ENOENT:
            raise

    run(['abcexport', full_path('%s.swf' % swf_name)])
    run(['rabcdasm', full_path('%s.abc' % abc_id)])
    subprocess.Popen([
        'patch', '-p0', '-i', '../asasm.patch'], cwd=full_path(abc_id)).wait()
    run(['rabcasm', full_path('%s/%s.main.asasm' % (abc_id, abc_id))])
    run([
        'abcreplace', full_path('%s.swf' % swf_name), str(abc_index),
        full_path('%s/%s.main.abc' % (abc_id, abc_id))])

if __name__ == '__main__':
    lock = threading.Lock()
    swf_path, swf_url = get_swf()
    patch_swf(swf_path)
    SeleniumRunner(lock).start()
    collected_data = run_server(swf_url, lock)
    enc_key = os.path.commonprefix(collected_data)
    print('enc_key = %s' % enc_key)

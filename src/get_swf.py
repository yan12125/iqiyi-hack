import contextlib
import errno
import importlib
import os
import os.path
import shutil
import subprocess
import threading
import sys

try:
    from urllib.request import urlretrieve as compat_urllib_request_urlretrieve
except ImportError:
    from urllib import urlretrieve as compat_urllib_request_urlretrieve

import urllib.parse as compat_urllib_parse

from server import run_server
from selenium_runner import SeleniumRunner
from common import full_path


def read_file(filename):
    with open(filename, 'rb') as f:
        data = f.read()
    return data


def write_file(filename, data):
    print(len(data))
    with open(filename, 'wb') as f:
        f.write(data)


def get_swf(target_site):
    swf_url = target_site.get_site_swf()
    parts = compat_urllib_parse.urlparse(swf_url)
    swf_path = full_path(os.path.basename(parts.path))
    compat_urllib_request_urlretrieve(swf_url, filename=swf_path)

    if hasattr(target_site, 'decrypt_swf'):
        old_swf_path = swf_path
        swf_path = os.path.splitext(swf_path)[0] + '_decrypted.swf'
        decrypted_swf = target_site.decrypt_swf(read_file(old_swf_path))
        write_file(swf_path, decrypted_swf)

    return swf_path, swf_url


def run(args):
    print(' '.join(args))
    subprocess.check_call(args)


@contextlib.contextmanager
def cd(path):
    old_path = os.getcwd()
    os.chdir(path)
    yield
    os.chdir(old_path)


def patch_swf(target_site, swf_path):
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
    with cd(full_path(abc_id)):
        run(['patch', '-i', os.path.join('..', target_site.PATCH_FILENAME)])
    run(['rabcasm', full_path('%s/%s.main.asasm' % (abc_id, abc_id))])
    run([
        'abcreplace', full_path('%s.swf' % swf_name), str(abc_index),
        full_path('%s/%s.main.abc' % (abc_id, abc_id))])


def main():
    lock = threading.Lock()

    site_name = sys.argv[1]
    target_site = importlib.import_module(site_name)

    swf_path, swf_url = get_swf(target_site)
    patch_swf(target_site, swf_path)
    SeleniumRunner(lock, target_site.PAGE_URL).start()
    collected_data = run_server(swf_path, swf_url, lock, target_site)
    enc_key = os.path.commonprefix(collected_data)
    print('enc_key = %s' % enc_key)

if __name__ == '__main__':
    main()

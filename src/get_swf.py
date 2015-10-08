import os
import os.path
import re
import shutil
import subprocess
import threading
import urllib.request

from config import PAGE_URL
from server import run_server
from selenium_runner import SeleniumRunner


def get_swf():
    print('Downloading the page %s' % PAGE_URL)
    urlh = urllib.request.urlopen(PAGE_URL)
    webpage = urlh.read().decode('utf-8')
    urlh.close()
    mobj = re.search(r'http://[^\'"]+MainPlayer[^.]+\.swf', webpage)
    swf_path = mobj.group(0)

    print('SWF path is %s' % swf_path)

    urllib.request.urlretrieve(swf_path, filename=os.path.basename(swf_path))
    return swf_path


def patch_swf(swf_name):
    swf_name = os.path.splitext(swf_name)[0]
    abc_index = 0
    abc_id = '%s-%d' % (swf_name, abc_index)

    try:
        os.remove('%s.abc' % abc_id)
        shutil.rmtree(abc_id)
    except FileNotFoundError:
        pass

    subprocess.check_call(['abcexport', '%s.swf' % swf_name])
    subprocess.check_call(['rabcdasm', '%s.abc' % abc_id])
    subprocess.Popen([
        'patch', '-p0', '-i', '../asasm.patch'], cwd=abc_id).wait()
    subprocess.check_call(['rabcasm', '%s/%s.main.asasm' % (abc_id, abc_id)])
    subprocess.check_call([
        'abcreplace', '%s.swf' % swf_name, str(abc_index),
        '%s/%s.main.abc' % (abc_id, abc_id)])

if __name__ == '__main__':
    lock = threading.Lock()
    swf_path = get_swf()
    patch_swf(os.path.basename(swf_path))
    SeleniumRunner(lock).start()
    collected_data = run_server(swf_path, lock)
    enc_key = os.path.commonprefix(collected_data)
    print('enc_key = %s' % enc_key)

import functools
import os.path
try:
    import http.server as compat_http_server
except ImportError:
    import BaseHTTPServer as compat_http_server

from config import PORT
from common import full_path


# BaseHTTPRequestHandler is an old-style class, which fails super()
# http://stackoverflow.com/a/11810015/3786245
class Handler(compat_http_server.BaseHTTPRequestHandler, object):
    def __init__(self, *args, **kwargs):
        swf_path = kwargs['swf_path']
        del kwargs['swf_path']

        self.swf_url = kwargs['swf_url']
        del kwargs['swf_url']

        self.collected_data = kwargs['collected_data']
        del kwargs['collected_data']

        self.target_site = kwargs['target_site']
        del kwargs['target_site']

        self.files_dict = {
            '/proxy.pac': full_path('proxy.pac'),
            self.swf_url: full_path(swf_path),
        }

        super(Handler, self).__init__(*args, **kwargs)

    def do_GET(self):
        if self.path in self.files_dict:
            self.send_response(200)
            self.end_headers()

            cur_file = self.files_dict[self.path]

            if os.path.exists(cur_file + '.in'):
                with open(cur_file + '.in', 'rb') as f:
                    content = f.read().decode('utf-8')
                content = (content.replace('$PORT$', str(PORT))
                                  .replace('$SWF_PATH$', self.swf_url)
                                  .replace('$DOMAIN$', self.target_site.DOMAIN))
                content = content.encode('utf-8')
            else:
                with open(cur_file, 'rb') as f:
                    content = f.read()
                    if hasattr(self.target_site, 'encrypt_swf'):
                        content = self.target_site.encrypt_swf(content)

            self.wfile.write(content)
        else:
            self.send_error(404)
            return

    def do_POST(self):
        length = int(self.headers.get('Content-Length', None))
        cur_data = self.rfile.read(length).decode('utf-8')
        self.send_response(200)
        self.end_headers()

        print(cur_data)
        self.collected_data.append(cur_data)

    def log_message(self, *args, **kwargs):
        pass


def run_server(swf_path, swf_url, lock, target_site, data_count=1):
    lock.acquire()

    collected_data = []

    httpd = compat_http_server.HTTPServer(
        ('', PORT), functools.partial(
            Handler, swf_path=swf_path, swf_url=swf_url,
            collected_data=collected_data, target_site=target_site))

    print('serving at port %d' % PORT)

    while len(collected_data) < data_count:
        httpd.handle_request()

    print('Proxy server done')
    lock.release()

    return collected_data

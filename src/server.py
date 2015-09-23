import http.server
import os.path
import json

with open('params.json', 'r') as f:
    params = json.load(f)


class Handler(http.server.BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        files = [
            params['swf_path'],
            '/proxy.pac',
        ]

        self.files_dict = {
            filename: os.path.basename(filename)
            for filename in files
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
                for k, v in params.items():
                    content = content.replace('$%s$' % k, str(v))
                content = content.encode('utf-8')
            else:
                with open(cur_file, 'rb') as f:
                    content = f.read()

            self.wfile.write(content)
        else:
            self.send_error(404)
            return

    def do_POST(self):
        length = int(self.headers.get('Content-Length', None))
        print(self.rfile.read(length))
        self.send_response(200)
        self.end_headers()


def main():
    port = params['port']

    httpd = http.server.HTTPServer(('', port), Handler)

    print('serving at port %d' % port)
    httpd.serve_forever()


if __name__ == '__main__':
    main()

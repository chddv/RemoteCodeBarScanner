from http.server import BaseHTTPRequestHandler
from urllib import parse
from os import curdir, path, sep
#from io

class RCBSRequestHandler(BaseHTTPRequestHandler):

    def do_GetPublic(self,html_path):
        file_path = curdir+sep+html_path

        # set mime type for return
        if file_path.endswith(".html"):
            mimetype='text/html'
        if file_path.endswith(".jpg"):
            mimetype='image/jpg'
        if file_path.endswith(".gif"):
            mimetype='image/gif'
        if file_path.endswith(".js"): 
            mimetype='application/javascript'
        if file_path.endswith(".css"):
            mimetype='text/css'

        #Open the static file requested and send it
        if path.exists(file_path):
            f = open(file_path, 'rb') 
            self.send_response(200)
            self.send_header('Content-type',mimetype)
            self.end_headers()
            self.wfile.write(f.read())
            f.close()
            return 
        # send error 404 if file not found
        self.send_error(404,'File Not Found: %s' % html_path)


    def do_GET(self):
        print('do_Get: '+self.path)
        parsed_path = parse.urlparse(self.path)
        splited_path = parsed_path.path.rsplit('/')
        if len(splited_path) >= 1:
            if(splited_path[1] == 'public'): # share only public files
                self.do_GetPublic(parsed_path.path)
            else:
                self.do_GetPublic("public/index.html")
        else:
            self.do_GetPublic("public/index.html")

'''
        message_parts = [
            'CLIENT VALUES:',
            'client_address={} ({})'.format(
                self.client_address,
                self.address_string()),
            'command={}'.format(self.command),
            'path={}'.format(self.path),
            'real path={}'.format(parsed_path.path),
            'query={}'.format(parsed_path.query),
            'request_version={}'.format(self.request_version),
            '',
            'SERVER VALUES:',
            'server_version={}'.format(self.server_version),
            'sys_version={}'.format(self.sys_version),
            'protocol_version={}'.format(self.protocol_version),
            '',
            'HEADERS RECEIVED:',
        ]
        for name, value in sorted(self.headers.items()):
            message_parts.append(
                '{}={}'.format(name, value.rstrip())
            )
        message_parts.append('')
        message = '\r\n'.join(message_parts)
        self.send_response(200)
        self.send_header('Content-Type',
                         'text/plain; charset=utf-8')
        self.end_headers()
        self.wfile.write(message.encode('utf-8'))
'''

if __name__ == '__main__':
    from http.server import HTTPServer
    server = HTTPServer(('localhost', 8080), RCBSRequestHandler)
    print('Starting server, use <Ctrl-C> to stop')
    server.serve_forever()
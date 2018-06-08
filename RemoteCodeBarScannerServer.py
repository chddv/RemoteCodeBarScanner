from http.server import BaseHTTPRequestHandler
from urllib import parse
from os import curdir, path, sep
#from io
import pyzbar.pyzbar as pyzbar
#import numpy as np
import cv2
import keyboard
import json

# library ZBar BarCode Reader http://zbar.sourceforge.net/download.html
# https://www.learnopencv.com/barcode-and-qr-code-scanner-using-zbar-and-opencv/
# https://pypi.org/project/zbar-py/

#library Keyboard https://pypi.org/project/keyboard/


class RCBSRequestHandler(BaseHTTPRequestHandler):

    srvIP = ''
    srvPort = ''

    def SetServerInfo(self, ip, port):
        srvIP = ip
        srvPort = port

    def do_Redirect(self, url):
        self.send_response(307)
        self.send_header('Location', url)
        self.end_headers()

    def do_GetPublic(self,html_path):
        file_path = curdir+sep+html_path
        print('do_GetPublic ' + file_path)

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
        else: # send error 404 if file not found
            print('File Not Found ' + html_path)
            self.send_error(404,'File Not Found: %s' % html_path)

    def do_GetAPI(self, msg):
        print(msg)
        keyboard.write(msg) #echo on keyboard (test of keyboard library)
        #echo on client web as json file 
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        jsonStr = json.dumps({'msg': msg})
        jsonByte = jsonStr.encode()
        self.wfile.write(jsonByte) 

    def do_GET(self):
        print('do_Get: '+self.path)
        parsed_path = parse.urlparse(self.path)
        splited_path = parsed_path.path.rsplit('/')
        print(splited_path)
        print(len(splited_path))
        if len(splited_path) >= 2: 
            if((splited_path[1] == 'public') and (splited_path[2] != '')): # share only public files
                self.do_GetPublic(parsed_path.path)
            elif((splited_path[1] == 'api') and (splited_path[2] != '')):
                self.do_GetAPI(splited_path[2])
            else:
                self.do_Redirect('/public/index.html')
        else:
            self.do_GetPublic('/public/index.html')

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
    srvIP = 'localhost'
    srvPort = 8080
    server = HTTPServer((srvIP, srvPort), RCBSRequestHandler)
    server.RequestHandlerClass.SetServerInfo(server.RequestHandlerClass, srvIP, srvPort)
    print('Starting server, use <Ctrl-C> to stop')
    server.serve_forever()

'''
#sample decode BarCode: 
def decode(im) : 
  # Find barcodes and QR codes
  decodedObjects = pyzbar.decode(im)
 
  # Print results
  for obj in decodedObjects:
    print('Type : ', obj.type)
    print('Data : ', obj.data,'\n')
     
  return decodedObjects

if __name__ == '__main__':
    im = cv2.imread("./img/sample001.jpg") #, cv2.IMREAD_GRAYSCALE)
    if(im is not None):
        decodedObjects = decode(im)
'''
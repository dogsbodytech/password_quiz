
import time
import string

from sys import version as python_version
from cgi import parse_header, parse_multipart

if python_version.startswith('3'):
    from urllib.parse import parse_qs
    from http.server import BaseHTTPRequestHandler
else:
    from urlparse import parse_qs
    from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer


HOST_NAME = 'localhost'
PORT_NUMBER = 8888
PASSWORD_FILE = 'passwords.txt'
DISPLAY_FILE = 'display.html'
DEFAULT_FILE = 'default.html'
FORM_FILE = 'form.html'
LAST_PASS = '????????'
LAST_POS ='??'


def ReturnFile(file):
    with open(file) as f:
        return f.read()


def ReturnHeader(s):
    s.send_response(200)
    s.send_header("Content-type", "text/html")
    s.end_headers()


def ReturnForm(s):
    s.wfile.write(FORM_HTML)


def ReturnDisplay(s):
    HTML = DISPLAY_HTML
    HTML = string.replace(HTML, 'PASSWORD-STRING', LAST_PASS, 1)
    HTML = string.replace(HTML, 'POSITION-STRING', LAST_POS, 1)
    s.wfile.write(HTML)


def ReturnDefault(s):
    s.wfile.write(DEFAULT_HTML)


class MyHandler(BaseHTTPRequestHandler):
    def parse_POST(self):
        ctype, pdict = parse_header(self.headers['content-type'])
        if ctype == 'multipart/form-data':
            postvars = parse_multipart(self.rfile, pdict)
        elif ctype == 'application/x-www-form-urlencoded':
            length = int(self.headers['content-length'])
            postvars = parse_qs(
                    self.rfile.read(length), 
                    keep_blank_values=1)
        else:
            postvars = {}
        return postvars
    def do_HEAD(s):
        ReturnHeader(s)
    def do_GET(s):
        ReturnHeader(s)
        if s.path == '/form':
            ReturnForm(s)
        elif s.path == '/display':
            ReturnDisplay(s)
        else:
            ReturnDefault(s)
    def do_POST(s):
        ReturnHeader(s)
        postvars = s.parse_POST()
        LAST_PASS = postvars['passguess']
        LAST_POS ='12'
        s.wfile.write(postvars)
        s.wfile.write('<br>')
        s.wfile.write(postvars['passguess'])
        ReturnForm(s)


if __name__ == '__main__':
    DISPLAY_HTML = ReturnFile(DISPLAY_FILE)
    DEFAULT_HTML = ReturnFile(DEFAULT_FILE)
    FORM_HTML = ReturnFile(FORM_FILE)
    server_class = HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
    print time.asctime(), "Server Starts - http://%s:%s" % (HOST_NAME, PORT_NUMBER)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print time.asctime(), "Server Stops - http://%s:%s" % (HOST_NAME, PORT_NUMBER)


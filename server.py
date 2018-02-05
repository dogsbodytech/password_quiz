
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
ENTRANTS_FILE = 'entries.txt'
PASSWORD_FILE = 'passwords/darkweb2017_top10K.txt'
DISPLAY_FILE = 'html/display.html'
DEFAULT_FILE = 'html/default.html'
FORM_FILE = 'html/form.html'
LAST_PASS = '????????'
LAST_POS ='??'


def ReturnFileContents(file):
    with open(file) as f:
        return f.read()


def AddToFile(file, results):
    with open(file, 'a') as output:
        output.write(results)


def ReturnHeader(id, content='text/html'):
    id.send_response(200)
    id.send_header("Content-type", content)
    id.end_headers()


def FindLineInFile(string):
    with open(PASSWORD_FILE) as myFile:
        for num, line in enumerate(myFile, 1):
            line = line.rstrip()
            if string == line:
                return num


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
            s.wfile.write(FORM_HTML)
        elif s.path == '/display':
            HTML = DISPLAY_HTML
            HTML = string.replace(HTML, 'PASSWORD-STRING', LAST_PASS, 1)
            HTML = string.replace(HTML, 'POSITION-STRING', str(LAST_POS), 1)
            s.wfile.write(HTML)
        else:
            s.wfile.write(DEFAULT_HTML)

    def do_POST(s):
        global LAST_PASS
        global LAST_POS
        ReturnHeader(s)
        postvars = s.parse_POST() # {'phone': [''], 'passguess': [''], 'name': [''], 'email': ['']} 
        LAST_PASS = postvars['passguess'][0]
        LAST_POS = FindLineInFile(LAST_PASS)
        logline = '{}|{}|{}|{}|{}|{}\n'.format(time.time(),LAST_PASS,LAST_POS,postvars['name'][0],postvars['email'][0],postvars['phone'][0])
        AddToFile(ENTRANTS_FILE, logline)
        s.wfile.write(FORM_HTML)


if __name__ == '__main__':
    DISPLAY_HTML = ReturnFileContents(DISPLAY_FILE)
    DEFAULT_HTML = ReturnFileContents(DEFAULT_FILE)
    FORM_HTML = ReturnFileContents(FORM_FILE)
    server_class = HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
    print time.asctime(), "Server Starts - http://%s:%s" % (HOST_NAME, PORT_NUMBER)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print time.asctime(), "Server Stops - http://%s:%s" % (HOST_NAME, PORT_NUMBER)



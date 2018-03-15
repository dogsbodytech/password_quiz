
import time
import string

from sys import version as python_version
from cgi import parse_header, parse_multipart

if python_version.startswith('3'):
    from urllib.parse import parse_qs
    from http.server import BaseHTTPRequestHandler, HTTPServer
else:
    from urlparse import parse_qs
    from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer


HOST_NAME = 'localhost'
PORT_NUMBER = 8888
ENTRANTS_FILE = 'entries.txt'
PASSWORD_FILE = 'passwords/darkweb2017_top10K.txt'
DISPLAY_FILE = 'html/display2.html'
DEFAULT_FILE = 'html/default.html'
BOOTSTRAP_FILE = 'html/bootstrap.min.css'
LOGO_FILE = 'html/dogsbodylogo.png'
FORM_FILE = 'html/form.html'
LAST_PASS = '??????????'
LAST_POS ='??'


def ReturnFileContents(file):
    with open(file) as f:
        return f.read()


def AddToFile(file, results):
    with open(file, 'a') as output:
        output.write(results)


def ReturnHeader(id, content='text/html', cache='no'):
    id.send_response(200)
    id.send_header("Content-type", content)
    if cache == "yes":
        id.send_header("Cache-Control", "public, max-age=31536000")
    else:
        id.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
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
        if s.path == '/display':
            ReturnHeader(s)
            HTML = DISPLAY_HTML
            HTML = string.replace(HTML, 'PASSSTRING', LAST_PASS, 1)
            HTML = string.replace(HTML, 'POSSTRING', str(LAST_POS), 1)
            s.wfile.write(HTML)
        elif s.path == '/form':
            ReturnHeader(s)
            s.wfile.write(FORM_HTML)
        elif s.path == '/bootstrap.min.css':
            ReturnHeader(s,"text/css", "yes")
            s.wfile.write(BOOTSTRAP_CSS)
        elif s.path == '/logo.png':
            ReturnHeader(s,"image/png", "yes")
            s.wfile.write(LOGO_PNG)
        else:
            ReturnHeader(s)
            s.wfile.write(DEFAULT_HTML) # This is the next thing that breaks in Python3

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
    BOOTSTRAP_CSS = ReturnFileContents(BOOTSTRAP_FILE)
    LOGO_PNG = ReturnFileContents(LOGO_FILE)
    FORM_HTML = ReturnFileContents(FORM_FILE)
    server_class = HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
    print('{} Server Starts - http://{}:{}'.format(time.asctime(), HOST_NAME, PORT_NUMBER))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print('{} Server Stops - http://{}:{}'.format(time.asctime(), HOST_NAME, PORT_NUMBER))



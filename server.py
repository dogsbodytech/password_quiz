
import time
import string
import cgi

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
RUDEWORDS_FILE = 'rudewords.txt'
PASSWORD_FILE = 'passwords/darkweb2017_top10K.txt'
DISPLAY_FILE = 'html/display.html'
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


def ReplaceStrings(text):
    CLEAN_PASS = (LAST_PASS[:20] + '..') if len(LAST_PASS) > 22 else LAST_PASS
    text = string.replace(text, 'PASSSTRING', LAST_PASS, 1)
    text = string.replace(text, 'POSSTRING', str(LAST_POS), 1)
    text = string.replace(text, 'CLEANPASS', CLEAN_PASS, 1)
    return text


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
            s.wfile.write(ReplaceStrings(DISPLAY_HTML))
        elif s.path == '/form':
            ReturnHeader(s)
            s.wfile.write(ReplaceStrings(FORM_HTML))
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
        postvars = s.parse_POST() # {'checkbox':[''],'passguess':[''],'name':[''],'email':['']} 
        LAST_PASS = cgi.escape(postvars['passguess'][0])
        LAST_POS = FindLineInFile(postvars['passguess'][0])
        LAST_NAME = postvars['name'][0]
        LAST_EMAIL = postvars['email'][0].lower()
        LAST_CHECK = 'off'
        if 'checkbox' in postvars:
            LAST_CHECK = postvars['checkbox'][0]
        logline = '{}|{}|{}|{}|{}|{}\n'.format(time.time(),LAST_PASS,LAST_POS,LAST_NAME,LAST_EMAIL,LAST_CHECK)
        AddToFile(ENTRANTS_FILE, logline)
        s.wfile.write(ReplaceStrings(FORM_HTML))


if __name__ == '__main__':
    DISPLAY_HTML = ReturnFileContents(DISPLAY_FILE)
    DEFAULT_HTML = ReturnFileContents(DEFAULT_FILE)
    BOOTSTRAP_CSS = ReturnFileContents(BOOTSTRAP_FILE)
    LOGO_PNG = ReturnFileContents(LOGO_FILE)
    FORM_HTML = ReturnFileContents(FORM_FILE)
    RUDEWORDS = ReturnFileContents(RUDEWORDS_FILE)
    server_class = HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
    print('{} Server Starts - http://{}:{}'.format(time.asctime(), HOST_NAME, PORT_NUMBER))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print('{} Server Stops - http://{}:{}'.format(time.asctime(), HOST_NAME, PORT_NUMBER))



import time
import BaseHTTPServer


HOST_NAME = 'localhost'
PORT_NUMBER = 8888
PASSWORDFILE = 'passwords.txt'
DISPLAY_FILE = 'display.html'
FORM_FILE = 'form.html'

DISPLAY_HTML = ReturnFile(DISPLAY_FILE)
FORM_HTML = ReturnFile(FORM_FILE)

def ReturnFile(file):
    with open(file) as f:
        return f.read()

def ReturnHeader(s):
    s.send_response(200)
    s.send_header("Content-type", "text/html")
    s.end_headers()

def ReturnDisplay(s):
    s.wfile.write(DISPLAY_HTML)

class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_HEAD(s):
         ReturnHeader(s)
    def do_GET(s):
        ReturnHeader(s)
        if s.path == '/form':
            s.wfile.write("<html><head><title>Form</title></head>")
            s.wfile.write("<body><p>This is a form.</p>")
            s.wfile.write("<p>You accessed path: %s</p>" % s.path)
            s.wfile.write("</body></html>")
        elif s.path == '/display':
            ReturnDisplay(s)
        else:
            s.wfile.write("<html><head><title>Default Page</title></head><body>")
            s.wfile.write("<p>Where would you like to go today?</p>")
            s.wfile.write("<p><a href=/form>The Form</a></p>")
            s.wfile.write("<p><a href=/display>The Display</a></p>")
            s.wfile.write("</body></html>")
    def do_POST(s):
        ReturnHeader(s)

if __name__ == '__main__':
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
    print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)

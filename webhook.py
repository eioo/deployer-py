#!/usr/bin/python3
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer


class Webhook(object):
    def __init__(self, callback, path='/git/webhook', port=1337):
        self.callback = callback
        self.path = path
        self.port = port
        self.running = False

    def listen(self):
        handler = make_webhook_handler(self.callback, self.path)
        httpd = HTTPServer(('localhost', self.port), handler)
        running = True

        print(f'Webhook created http://localhost:{self.port}{self.path}')

        def listen_loop():
            while running:
                httpd.handle_request()

            httpd.server_close()
            print('Webhook closed')

        t = threading.Thread(target=listen_loop)
        t.start()

    def stop(self):
        self.running = False


def make_webhook_handler(webhook_callback, webhook_path):
    class RequestHandler(BaseHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super(RequestHandler, self).__init__(*args, **kwargs)

        def do_GET(self):
            if self.path == webhook_path:
                t = threading.Thread(target=webhook_callback)
                t.start()

                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(bytes('<html><body>OK</body></html>'.format(self.path), 'UTF-8'))

        def log_message(self, f, *args):
            return

    return RequestHandler

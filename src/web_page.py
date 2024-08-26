#!/usr/bin/env python3


# web_page.py

import os
from functools import cached_property
from http.cookies import SimpleCookie
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qsl, urlparse

class WebRequestHandler(BaseHTTPRequestHandler):
    @cached_property
    def url(self):
        return urlparse(self.path)

    @cached_property
    def query_data(self):
        return dict(parse_qsl(self.url.query))

    @cached_property
    def post_data(self):
        content_length = int(self.headers.get("Content-Length", 0))
        return self.rfile.read(content_length)

    @cached_property
    def form_data(self):
        return dict(parse_qsl(self.post_data.decode("utf-8")))

    @cached_property
    def cookies(self):
        return SimpleCookie(self.headers.get("Cookie"))

    def do_GET(self):
        try:
            self.send_response(200)
            if self.path == "/":
                self.path = "/web/"
            if self.path.endswith("/"):
                self.path += "index.html"
            if (self.path.endswith(".html")):
                self.send_header("Content-type", "text/html")
            elif (self.path.endswith(".css")):
                self.send_header("Content-type", "text/css")
            elif self.path.endswith("favicon.ico"):
                self.send_header('Content-Type', 'image/x-icon')
                self.send_header('Content-Length', 0)
                self.end_headers()
                return
            elif self.path.endswith(".png"):
                self.send_header('Content-Type', 'image/png')
            elif self.path.endswith(".jpg"):
                self.send_header('Content-Type', 'image/jpg')
            self.end_headers()
            self.wfile.write(bytes(self.get_response(os.path.join('.', self.path[1:]))))
        except IOError:
            self.send_error(404, "File Not Found: %s" % self.path)

    def do_POST(self):
        self.do_GET()

    def get_response(self, file):
        data = b""
        with open(file, 'rb') as file:
            data += file.read()
        return data

# Throw an error if run directly.
try:
    assert __name__ != "__main__"
except AssertionError:
    from err import throw
    throw(RuntimeError, "0x02", "Please run from run.py.")
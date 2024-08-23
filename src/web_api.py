#!/usr/bin/env python3


# web_api.py

import json, re
import sql_server
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

    def do_POST(self):
        path, match = self.get_path()
        item_created = None
        if path == "root birds":
            item_created = sql_server.create_bird(sql_server.session, self.form_data)
        self.get_response(item_created)

    def do_GET(self):
        path, match = self.get_path()
        item_found = None
        if path == "root birds":
            item_found = sql_server.read_birds(sql_server.session)
        elif path == "bird id":
            item_found = sql_server.read_bird(sql_server.session, match.group(1))
        self.get_response(item_found)

    def do_PUT(self):
        path, match = self.get_path()
        item_updated = None
        if path == "bird id":
            item_updated = sql_server.update_bird(sql_server.session, match.group(1), self.form_data)
        self.get_response(item_updated)

    def do_DELETE(self):
        path, match = self.get_path()
        item_deleted = None
        if path == "bird id":
            item_deleted = sql_server.delete_bird(sql_server.session, match.group(1))
        self.get_response(item_deleted)

    def get_path(self):
        root = re.compile(r"^/birds/?$")
        sub = re.compile(r"^/birds/(\d+)/?$")
        path = "root birds"
        match = root.fullmatch(self.url.path)
        if match is None:
            path, match = "bird id", sub.fullmatch(self.url.path)
        if match is None:
            path = None
        return path, match

    def get_response(self, output):
        if output is not None:
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            if isinstance(output, dict):
                self.wfile.write(json.dumps(output).encode("utf-8"))
            elif isinstance(output, list):
                self.wfile.write(json.dumps([item.as_dict() for item in output]).encode("utf-8"))
            else:
                self.wfile.write(json.dumps(output.as_dict()).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()
            response = {"message": "Item not found."}
            self.wfile.write(json.dumps(response).encode("utf-8"))

# Throw an error if run directly.
try:
    assert __name__ != "__main__"
except AssertionError:
    from err import throw
    throw(RuntimeError, "0x02", "Please run from run.py.")
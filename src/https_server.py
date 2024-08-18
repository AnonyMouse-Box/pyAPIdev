#!/usr/bin/env python3


# https_server.py

import argparse
import webbrowser
from http.server import HTTPServer
from ssl import PROTOCOL_TLS_SERVER, SSLContext

import web_page
from self_signed import SelfSignedCertificate

def main(args, session=None):
  ssl_context = SSLContext(PROTOCOL_TLS_SERVER)
  ssl_context.load_cert_chain(SelfSignedCertificate(args.host).path)
  server = HTTPServer((args.host, args.port), web_page.WebRequestHandler)
  server.socket = ssl_context.wrap_socket(server.socket, server_side=True)
  webbrowser.open(f"https://{args.host}:{args.port}/")
  server.serve_forever()

def parse_args():
  parser = argparse.ArgumentParser()
  parser.add_argument("--host", type=str, default="0.0.0.0")
  parser.add_argument("--port", type=int, default=443)
  return parser.parse_args()

# Throw an error if run directly.
try:
    assert __name__ != "__main__"
except AssertionError:
    from err import throw
    throw(RuntimeError, "0x02", "Please run from run.py.")
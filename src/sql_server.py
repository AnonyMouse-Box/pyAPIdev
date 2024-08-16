#!/usr/bin/env python3


# sql_server.py

def main():
    print("running sql_server.py")


# Throw an error if run directly.
try:
    assert __name__ != "__main__"
except AssertionError:
    from err import throw
    throw(RuntimeError, "0x02", "Please run from run.py.")
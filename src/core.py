#!/usr/bin/env python3


# core.py

import https_server

def main(argv: list[str]) -> int:
    """
    Main function for processing stages.
    :param argv: A list of arguments containing the program name and the user choice.
    :return: An exit code signifying the status upon completion.
    :rtype: int
    """
    try:
        assert argv[0] == "run.py"
    except AssertionError as e:
        from err import throw
        throw(SyntaxError, "0x09", "Invalid argument.")
    print("Booting software...")
    
    https_server.main(https_server.parse_args())

    print("Shutting down...")
    return 0

# Throw an error if run directly.
try:
    assert __name__ != "__main__"
except AssertionError:
    from err import throw
    throw(RuntimeError, "0x02", "Please run from run.py.")
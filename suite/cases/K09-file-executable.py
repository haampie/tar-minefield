"""An executable file.

The archive has two files: `r`, with the mode 644, and `x`, a shell script with the mode 755.

The [mode][mode] field contains the permissions of a file, of which one is the execute permission of
its owner. A script or a program does not run without that permission, so whether a file is
executable is part of the tree. The file `x` is executable, and `r` is not. A reader that creates
every file with the same mode extracts `x` without it.

Seen in: tarballs with scripts and programs, such as `configure`.
"""
F = lambda path, contents: {"path": path, "kind": "file", "contents": contents, "executable": False}
X = lambda path, contents: {"path": path, "kind": "file", "contents": contents, "executable": True}

VERDICT = "accept"
ID = "K09"
FEATURES = []
TREE = [F("r", b"r\n"), X("x", b"#!/bin/sh\n")]


def build(a):
    a.file(b"r", b"r\n")
    a.file(b"x", b"#!/bin/sh\n", mode=0o755, note="executable")
    a.end()

"""An executable file.

The archive has two files: `r` with mode 644, and `x`, a shell script with mode 755.

The [mode][mode] field stores a file's permission bits, including whether its owner may execute it.
Because scripts and binaries cannot run without that bit, the expected tree records whether each
file is executable: `x` is executable and `r` is not. A reader that ignores the mode field and
creates all files with default permissions leaves `x` non-executable.

Seen in: tarballs containing scripts or binaries, such as `configure`.
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

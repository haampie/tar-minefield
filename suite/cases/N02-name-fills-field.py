"""A name of exactly 100 bytes, which fills the name field without a NUL.

The archive has one file whose name is 100 `n`s, which fill the name field without a NUL.

In [POSIX][name-full], the name field ends with a NUL except when all of its bytes are non-NUL, so
the name is all 100 bytes.

Seen in: thousands of tarballs.
"""

F = lambda path, contents: {"path": path, "kind": "file", "contents": contents, "executable": False}

VERDICT = "accept"
ID = "N02"
FEATURES = []
TREE = [F('nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn', b'full\n')]


def build(a):
    a.file(b"nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn", b"full\n")
    a.end()

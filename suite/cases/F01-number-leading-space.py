"""Number fields padded with spaces rather than zeros, as old tars wrote them.

Seen in: hundreds of tarballs, many from CPAN.
"""

F = lambda path, contents: {"path": path, "kind": "file", "contents": contents, "executable": False}

VERDICT = "accept"
ID = "F01"
FEATURES = []
TREE = [F('a', b'spaces\n')]


def build(a):
    a.file(b"a", b"spaces\n", mode=b"   644 \0", uid=b"     0 \0", gid=b"     0 \0",
           size=b"          7 ", mtime=b"          0 ")
    a.end()

"""Numeric fields padded with spaces rather than zeros, as old tars wrote them.

The mode, uid, gid, size and mtime fields are padded with spaces, such as `          7 ` for the
size of `a`. In POSIX, numeric fields are leading zero-filled octal numbers.

Seen in: hundreds of tarballs, many from CPAN.
"""

F = lambda path, contents: {"path": path, "kind": "file", "contents": contents, "executable": False}

VERDICT = "tolerate"
ID = "F01"
FEATURES = ["number.mode.leading-space", "number.size.leading-space"]
POSIX = "zero-filled"
TREE = [F('a', b'spaces\n')]


def build(a):
    a.file(b"a", b"spaces\n", mode=b"   644 \0", uid=b"     0 \0", gid=b"     0 \0",
           size=b"          7 ", mtime=b"          0 ")
    a.end()

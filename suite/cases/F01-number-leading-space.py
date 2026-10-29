"""Numeric fields padded with spaces rather than zeros, as old tars wrote them.

The archive has one file, `a`, whose mode, uid, gid, size and mtime fields are padded with spaces
rather than zeros, such as ` 7 ` for its size.

In [POSIX][zero-filled], numeric fields are octal numbers filled with leading zeros.

Seen in: hundreds of tarballs, many from CPAN, which pad the checksum with spaces too.
See also: F32, a checksum padded with spaces, as those tarballs have it.
"""

F = lambda path, contents: {"path": path, "kind": "file", "contents": contents, "executable": False}

VERDICT = "tolerate"
ID = "F01"
FEATURES = ["number.mode.leading-space", "number.size.leading-space"]
TREE = [F('a', b'spaces\n')]


def build(a):
    a.file(b"a", b"spaces\n", mode=b"   644 \0", uid=b"     0 \0", gid=b"     0 \0",
           size=b"          7 ", mtime=b"          0 ")
    a.end()

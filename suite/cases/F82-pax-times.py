"""A pax header with the times of a file, with fractions of a second, as GNU tar writes it.

The archive has a file `a`, whose pax header has the records `mtime=1700000000.123456789`,
`atime=1700000001.5` and `ctime=1700000002.000000001`.

In POSIX, the records `mtime` and `atime` are [decimal numbers of seconds][time-decimal], which can
have a decimal point and digits after it. The key `ctime` was removed from POSIX in 2004, and GNU
tar writes it in the same format: in an archive in the pax format, it writes `atime` and `ctime` for
every member, and `mtime` when it has a fraction of a second. Times are not part of the tree.

Seen in: hundreds of tarballs, made by GNU tar in the pax format.
"""
F = lambda path, contents: {"path": path, "kind": "file", "contents": contents, "executable": False}

VERDICT = "accept"
ID = "F82"
FEATURES = []
TREE = [F("a", b"a\n")]


def build(a):
    a.pax([(b"mtime", b"1700000000.123456789"), (b"atime", b"1700000001.5"),
           (b"ctime", b"1700000002.000000001")], note="times with fractions")
    a.file(b"a", b"a\n")
    a.end()

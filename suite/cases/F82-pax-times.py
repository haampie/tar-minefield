"""Subsecond `mtime`, `atime` and `ctime` records in a pax header, as written by GNU tar.

The archive has a file `a` whose pax header sets `mtime=1700000000.123456789`, `atime=1700000001.5`
and `ctime=1700000002.000000001`.

In POSIX, `mtime` and `atime` are [decimal seconds since the Epoch][time-decimal] with an optional
fractional part. Although POSIX removed `ctime` in 2004, GNU tar still writes `atime` and `ctime` in
pax archives for every member, plus `mtime` whenever the modification time has a subsecond fraction.
Timestamps are not part of the extracted tree.

Seen in: hundreds of tarballs created by GNU tar in pax format.
"""
F = lambda path, contents: {"path": path, "kind": "file", "contents": contents, "executable": False}

VERDICT = "accept"
ID = "F82"
FEATURES = []
TREE = [F("a", b"a\n")]


def build(a):
    a.pax([(b"mtime", b"1700000000.123456789"), (b"atime", b"1700000001.5"),
           (b"ctime", b"1700000002.000000001")], note="subsecond timestamps")
    a.file(b"a", b"a\n")
    a.end()

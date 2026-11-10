"""A uid and a gid in base-256, as GNU tar writes those over 2097151.

The archive has a file `a` with GNU's magic, whose uid and gid fields are 3000000 in base-256: the
byte `0x80`, followed by the number in binary.

A uid or gid over 2097151 does not fit in the 7 octal digits of its field. In pax, it is written in
a [record][uid-large] of the extended header. In GNU's format, it is written in base-256, as a size
of 8 GiB and over is. The owner of a file is not part of the tree, so a reader need not read the
number, and every implementation must extract `a`.

Seen in: 214 of the scanned tarballs.
See also: F56, a size in base-256.
"""
F = lambda path, contents: {"path": path, "kind": "file", "contents": contents, "executable": False}

VERDICT = "accept"
ID = "F80"
FEATURES = ["number.uid.base256", "number.gid.base256"]
TREE = [F("a", b"a\n")]


def build(a):
    number = b"\x80" + (3000000).to_bytes(7, "big")
    a.file(b"a", b"a\n", uid=number, gid=number, magic=b"ustar ", version=b" \0",
           note="uid and gid 3000000, in base-256")
    a.end()

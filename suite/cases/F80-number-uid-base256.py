"""Base-256 uid and gid fields, as GNU tar writes for IDs over 2097151.

The archive has a file `a` with GNU magic whose uid and gid fields encode 3000000 in base-256: a
leading `0x80` byte followed by a 7-byte big-endian integer.

A user or group ID above 2097151 overflows a 7-digit octal field. The pax format stores large IDs in
[extended header records][uid-large], whereas GNU tar encodes them in base-256, just like file sizes
of 8 GiB or more. Because ownership is not part of the extracted tree, a reader need not use these
values, and every implementation must extract `a`.

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
           note="uid and gid 3000000 in base-256")
    a.end()

"""A size of 512 in base-256.

The archive has a file `a` of 512 bytes, whose size field is in base-256: the byte 0x80, followed
by 512 as a binary number.

Sizes of 8 GiB and over do not fit in the 11 octal digits of the size field. In pax, they are
written in a `size` record. In GNU's format, they are written in base-256, which its first byte
tells apart from octal. In [POSIX][zero-filled], numeric fields are octal, so base-256 is an
extension. This case is tolerated because it has one reading, here 512: a reader that does not
support base-256 cannot take it for octal. It is a small instance of the base-256 sizes of large
files, which no case can contain.

Seen in: none of the scanned tarballs.
See also: F29 and F30, a negative size and a size past 64 bits, in base-256.
"""
F = lambda path, contents: {"path": path, "kind": "file", "contents": contents, "executable": False}

VERDICT = "tolerate"
ID = "F57"
FEATURES = ["number.size.base256"]
TREE = [F("a", b"a\n" * 256)]


def build(a):
    a.header(b"a", b"0", b"\x80" + (512).to_bytes(11, "big"), note="size 512, in base-256")
    a.data(b"a\n" * 256)
    a.end()

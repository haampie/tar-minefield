"""An archive that ends inside a header.

The archive has a file `a`, followed by the first 300 bytes of a header for a file `b`, where the
archive ends.

Every POSIX header is a [512-byte block][block-512], so this archive is truncated. Most readers
report an error on the partial block. A reader that treats a short read as the end of the archive
stops after extracting `a`, while one that parses the 300 available bytes as a header extracts both
`a` and an empty `b`.

Decision point: whether a truncated header at the end of an archive is treated as EOF.
Seen in: none of the scanned tarballs.
See also: F08, an archive that ends inside file data, and F04, one that ends after a complete
member.
"""

VERDICT = "reject"
ID = "F64"
FEATURES = []


def build(a):
    a.file(b"a", b"a\n")
    header = type(a)().header(b"b", b"0", 0).bytes()
    a.cut(header[:300], "header: the first 300 of its 512 bytes, of a file b")

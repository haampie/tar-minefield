"""An archive that ends inside a header.

The archive has a file `a`, then the first 300 bytes of the header of a file `b`, and ends there.

In POSIX, a header is a [block of 512 bytes][block-512], so the archive is cut short. This case is
ambiguous in practice because a reader can take the 300 bytes in one of three ways. A reader that
takes an incomplete block for the end of the archive extracts `a`, without an error. One that reads
a header from the bytes that are there extracts `a` and an empty `b`. Other readers report an error.

Decision point: whether a header that is cut short ends the archive.
Seen in: none of the scanned tarballs.
See also: F08, an archive that ends inside the data of a member, and F04, one that ends after a
complete member.
"""

VERDICT = "reject"
ID = "F64"
FEATURES = []


def build(a):
    a.file(b"a", b"a\n")
    header = type(a)().header(b"b", b"0", 0).bytes()
    a.cut(header[:300], "header: the first 300 of its 512 bytes, of a file b")

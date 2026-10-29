"""A checksum that only matches as the signed sum of the header.

The archive has one file, `a`, with the byte 0xe9 in its `uname`, and a checksum that is the sum of
the bytes of its header taken as signed numbers.

In [POSIX][checksum], the checksum is the sum of the bytes of a header taken as unsigned numbers.
Some old tars added them as signed. With a byte over 127 in the header, the two totals differ, and
the checksum matches only the signed one. This case is ambiguous because a reader takes the header
in one of three ways: as valid, by the signed sum, and extracts `a`; as invalid, and stops; or as
invalid, and skips ahead to the next header.

Decision point: whether a signed checksum makes a header valid.
Seen in: none of the scanned tarballs.
"""

VERDICT = "reject"
ID = "F06"
FEATURES = ['checksum.signed']


def build(a):
    a.file(b"a", b"a\n", uname=b"\xe9", chksum="signed", note="a byte over 127 in uname")
    a.end()

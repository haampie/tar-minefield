"""A checksum that only matches as the signed sum of the header.

In POSIX, the checksum is the sum of the bytes of a header taken as unsigned numbers. Some old tars
added them as signed, and many implementations still accept either. With a byte over 127 in the
header, here in `uname`, the two totals differ, and the checksum matches only the signed one. This
case is ambiguous because a reader takes the header in one of three ways: as valid, by the signed
sum, and extracts `a`; as invalid, and stops; or as invalid, and skips ahead to the next header, as node-tar does
before it fails for want of one.

Decision point: whether a signed checksum makes a header valid.
Seen in: none of the scanned tarballs.
"""

VERDICT = "reject"
ID = "F06"
FEATURES = ['checksum.signed']
POSIX = "checksum"


def build(a):
    a.file(b"a", b"a\n", uname=b"\xe9", chksum="signed", note="a byte over 127 in uname")
    a.end()

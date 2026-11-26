"""A checksum that only matches as the signed sum of the header.

The archive has one file, `a`, with the byte `0xe9` in its `uname` field and a checksum computed as
the signed sum of the header bytes.

In [POSIX][checksum], the checksum is the sum of the header bytes treated as unsigned values,
whereas some old tars summed them as signed bytes. Because the header contains a byte over 127, the
two sums differ and the checksum matches only the signed total. A reader that accepts the signed sum
extracts `a`, whereas one that requires an unsigned sum rejects the header and either stops or skips
ahead to the next header.

Decision point: whether a signed checksum makes a header valid.
Seen in: none of the scanned tarballs.
"""

VERDICT = "reject"
ID = "F06"
FEATURES = ['checksum.signed']


def build(a):
    a.file(b"a", b"a\n", uname=b"\xe9", chksum="signed", note="a byte over 127 in uname")
    a.end()

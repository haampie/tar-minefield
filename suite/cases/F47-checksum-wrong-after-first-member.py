"""A header with a wrong checksum after the first member: the end, a block to skip, or a header?

The archive has a file `a`, a header for a 512-byte file `b` with an invalid checksum of 0, a
512-byte block (`b`'s data) that forms a valid header for an empty file `smuggled`, and finally a
file `c`.

In POSIX, a header's [checksum][checksum-sum] is the sum of its bytes, and the behavior on a
checksum mismatch is unspecified. A reader that treats a bad header as the end of the archive stops
and extracts only `a`. A reader that scans forward for the next block with a valid checksum lands on
`smuggled` and extracts `a`, `smuggled` and `c`. A reader that does not verify checksums extracts
`a`, `b` and `c`.

Decision point: what a reader does after a header whose checksum is wrong.
Seen in: none of the scanned tarballs.
See also: F06, a checksum that matches only as a signed sum.
"""

VERDICT = "reject"
ID = "F47"
FEATURES = []


def build(a):
    a.file(b"a", b"a\n")
    a.header(b"b", b"0", 512, chksum=b"000000\0 ", note="checksum 0, which is wrong")
    a.file(b"smuggled", b"", note="the data of b, or a header found by skipping a bad block")
    a.file(b"c", b"c\n")
    a.end()

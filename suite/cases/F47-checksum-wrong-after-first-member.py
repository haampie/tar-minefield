"""A header with a wrong checksum after the first member: the end, a block to skip, or a header?

The archive has a file `a`, then a header of a file `b` of 512 bytes whose checksum is 0, which is
wrong, then a block that is the header of an empty file `smuggled`, as the data of `b`, then a file
`c`.

In POSIX, the [checksum][checksum-sum] is a sum of the bytes of the header, but it is not said what
a reader does with a header whose checksum is wrong. This case is ambiguous because a reader can
take the header in one of three ways. A reader that takes it for the end of the archive extracts
`a`. One that skips blocks until it finds a header with a correct checksum extracts `a`, `smuggled`
and `c`. One that does not check the checksum extracts `a`, `b` and `c`.

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

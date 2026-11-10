"""A checksum with a NUL before its digits, in a header after the first member.

The archive has the files `a`, `b` and `c`. The checksum field of `b` is a NUL, followed by six
octal digits, followed by a NUL. The digits are the correct sum.

In [POSIX][zero-filled], numeric fields are octal numbers filled with leading zeros, and each is
[terminated][numeric] by a space or a NUL. This case is ambiguous in practice because a reader can
take the header of `b` in one of four ways. A reader that skips the NUL in front finds the correct
sum, and extracts `a`, `b` and `c`. One that ends the number at its first NUL does not find the sum;
if it takes a header with a wrong checksum for the end of the archive, it extracts `a`, without an
error. One that skips blocks until it finds a header with a correct checksum extracts `a` and `c`.
Other readers report an error.

Decision point: how a checksum with a NUL before its digits is read.
Seen in: none of the scanned tarballs.
See also: F41, a size with a NUL before its digits, and F47, a header with a wrong checksum after
the first member.
"""

VERDICT = "reject"
ID = "F77"
FEATURES = ["number.chksum.leading-nul"]


def build(a):
    a.file(b"a", b"a\n")
    a.file(b"b", b"b\n", chksum=lambda total: b"\0%06o\0" % total,
           note="its checksum starts with a NUL")
    a.file(b"c", b"c\n")
    a.end()

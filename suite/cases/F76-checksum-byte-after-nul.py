"""A byte after the NUL that ends a checksum, in a header after the first member.

The archive has the files `a`, `b` and `c`. The checksum field of `b` is six octal digits, followed
by a NUL, followed by the letter `x`. The digits are the correct sum.

In POSIX, a numeric field is [terminated][numeric] by one or more spaces or NULs, and the checksum
field has 8 bytes. It is not specified what may follow the terminator. Most writers end the six
digits with a NUL and a space, and here the last byte is the letter `x`. This case is ambiguous in
practice because a reader can take the header of `b` in one of three ways. A reader that reads the
digits up to the NUL finds the correct sum, and extracts `a`, `b` and `c`. One that checks every
byte of the field does not take the block for a header, and skips to the next one that it
recognizes: it extracts `a` and `c`, without an error. Other readers report an error.

Decision point: whether the bytes after the terminator of a checksum are part of it.
Seen in: not measured, as earlier versions of the scanner did not report it: at most 7 of the
scanned tarballs have a checksum field with a byte that is not a digit, a space or a NUL.
See also: F47, a header with a wrong checksum after the first member, and F32, a checksum padded
with spaces.
"""

VERDICT = "reject"
ID = "F76"
FEATURES = ["number.chksum.invalid-character"]


def build(a):
    a.file(b"a", b"a\n")
    a.file(b"b", b"b\n", chksum=lambda total: b"%06o\0x" % total,
           note="its checksum ends in a NUL and x")
    a.file(b"c", b"c\n")
    a.end()

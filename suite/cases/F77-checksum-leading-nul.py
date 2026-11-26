"""A checksum with a leading NUL before its digits, after the first member.

The archive has three files, `a`, `b` and `c`. In `b`'s checksum field, a leading NUL precedes the
six octal digits of the valid sum and a trailing NUL.

In [POSIX][zero-filled], numeric fields are leading-zero-filled octal numbers [terminated][numeric]
by a space or a NUL. A reader that skips leading NULs parses the checksum and extracts `a`, `b` and
`c`. A reader that stops at the first NUL sees an empty checksum: it may report an error, treat the
bad header as the end of the archive and extract only `a`, or scan forward to the next valid header
and extract `a` and `c`.

Decision point: how a leading NUL in the checksum field is handled.
Seen in: none of the scanned tarballs.
See also: F41, a size with a leading NUL, and F47, a bad checksum after the first member.
"""

VERDICT = "reject"
ID = "F77"
FEATURES = ["number.chksum.leading-nul"]


def build(a):
    a.file(b"a", b"a\n")
    a.file(b"b", b"b\n", chksum=lambda total: b"\0%06o\0" % total,
           note="checksum starts with NUL")
    a.file(b"c", b"c\n")
    a.end()

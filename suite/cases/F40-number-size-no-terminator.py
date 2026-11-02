"""A size of 12 octal digits, without a terminator.

The archive has one file, `a`, whose size field is the 12 octal digits `000000000012`, without a
NUL or a space after them, and whose data is the 10 bytes `0123456789`.

In [POSIX][numeric], every numeric field is terminated by a space or a NUL, so a size of 12 digits
has no room for its terminator. A reader that takes the whole field reads 10, octal 12; a reader
that takes at most the 11 digits that ustar allows reads 1. This case is ambiguous because `a` is
`0123456789` or `0`; both fit in the one block of data, so the rest of the archive is read alike.

Decision point: whether a numeric field without a terminator is read to its end.
Seen in: none of the scanned tarballs.
See also: F12, a size with a gap in its digits.
"""

VERDICT = "reject"
ID = "F40"
FEATURES = ["number.size.no-terminator"]


def build(a):
    a.file(b"a", b"0123456789", size=b"000000000012", note="12 digits, without a terminator")
    a.end()

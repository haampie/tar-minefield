"""A size of 12 octal digits, without a terminator.

The archive has one file, `a`, whose size field is the 12 octal digits `000000000012`, without a
NUL or a space after them, and whose data is the 10 bytes `0123456789`.

In [POSIX][numeric], every numeric field is terminated by a space or a NUL, so a size of 12 digits
is invalid and does not leave room for a terminator. A lenient reader can either read 10 (octal 12)
or 1 if it takes the 11 digits that ustar allows, assuming the last byte is a terminator.

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

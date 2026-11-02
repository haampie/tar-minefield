"""A size of 12 octal digits, without a terminator.

The archive has one file, `a`, whose size field is the 12 octal digits `000000000012`, without a
NUL or a space after them, and whose data is the 10 bytes `0123456789`.

In [POSIX][numeric], every numeric field is terminated by a space or a NUL, so a size of 12 digits
is invalid, as it does not leave room for a terminator. Read leniently, this case is ambiguous
because the size is either 10, octal 12, if the field is read to its end (and `a` contains
`0123456789`), or 1, if its last byte is taken for a terminator (and `a` contains `0`).

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

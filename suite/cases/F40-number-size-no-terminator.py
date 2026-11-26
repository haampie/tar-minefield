"""A size of 12 octal digits, without a terminator.

The archive has one file, `a`, with 10 bytes of data (`0123456789`) and 12 octal digits
(`000000000012`) filling its size field without a trailing NUL or space.

In [POSIX][numeric], every numeric field ends with at least one space or NUL, so a 12-digit size is
invalid because it leaves no room for a terminator. A lenient reader that parses all 12 bytes reads
octal 12 (10) and extracts `0123456789`, whereas one that treats the 12th byte as a terminator reads
octal 1 and extracts only `0`.

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

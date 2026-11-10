"""A uid with the digit 8, in a header after the first member.

The archive has the files `a`, `b` and `c`. The uid field of `b` is `0000008`.

In [POSIX][zero-filled], numeric fields are octal numbers filled with leading zeros, and 8 is not an
octal digit. The [owner][uid-gid] of a file is not part of the tree, but its field is part of the
header. This case is ambiguous in practice because a reader can take the header of `b` in one of
three ways. A reader that does not read the uid, or that reads it up to the 8, extracts `a`, `b` and
`c`. One that takes a header with a field that is not a number for the end of the archive extracts
`a`, without an error. Other readers report an error.

Decision point: whether a header with a uid that is not a number is a header.
Seen in: none of the scanned tarballs.
See also: F37, a size with the digit 9, and F47, a header with a wrong checksum after the first
member.
"""

VERDICT = "reject"
ID = "F61"
FEATURES = ["number.uid.invalid-character"]


def build(a):
    a.file(b"a", b"a\n")
    a.file(b"b", b"b\n", uid=b"0000008\0", note="a uid that is not octal")
    a.file(b"c", b"c\n")
    a.end()

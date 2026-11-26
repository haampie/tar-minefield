"""A uid with the digit 8, in a header after the first member.

The archive has three files, `a`, `b` and `c`, with `0000008` in `b`'s uid field.

In [POSIX][zero-filled], numeric fields are leading-zero-filled octal numbers, so 8 is invalid. A
file's [owner][uid-gid] is not part of the extracted tree, yet the uid field is still part of the
header. A reader that ignores the uid or stops parsing it at the 8 extracts `a`, `b` and `c`. A
reader that treats a header with an invalid number as the end of the archive stops and extracts only
`a`. Other readers reject the archive.

Decision point: whether a header with a non-octal uid is valid.
Seen in: none of the scanned tarballs.
See also: F37, a size with the digit 9, and F47, a bad checksum after the first member.
"""

VERDICT = "reject"
ID = "F61"
FEATURES = ["number.uid.invalid-character"]


def build(a):
    a.file(b"a", b"a\n")
    a.file(b"b", b"b\n", uid=b"0000008\0", note="non-octal uid")
    a.file(b"c", b"c\n")
    a.end()

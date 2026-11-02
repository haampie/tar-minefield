"""A size with a NUL before its digits, which takes the next header for its data.

The archive has a file `a`, whose size field is a NUL, followed by the digits `0000001000`, followed
by a NUL, then an empty file `smuggled`.

In [POSIX][zero-filled], numeric fields are octal numbers filled with leading zeros, and each is
[terminated][numeric] by a space or a NUL. Read leniently, this case is ambiguous because the size
is either 512, octal 1000, if the NUL in front is skipped (and the next block is the data of `a`),
or 0, if the field ends at its first NUL (and the next block is the header of `smuggled`).

Decision point: how a numeric field with a NUL before its digits is read.
Seen in: none of the scanned tarballs.
"""

VERDICT = "reject"
ID = "F41"
FEATURES = ["number.size.leading-nul"]


def build(a):
    a.header(b"a", b"0", b"\x000000001000\x00", note="a NUL, then 512 in octal")
    a.file(b"smuggled", b"", note="the data of a, to a reader that skips the NUL")
    a.end()

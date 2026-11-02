"""A size with a NUL before its digits, which takes the next header for its data.

The archive has a file `a`, whose size field is a NUL, followed by the digits `0000001000`, followed
by a NUL, then an empty file `smuggled`.

In [POSIX][zero-filled], numeric fields are octal numbers filled with leading zeros, and each is
[terminated][numeric] by a space or a NUL. A reader that skips the NUL in front reads 512, octal
1000, and takes the block after the header of `a` for its data; a reader that stops at the first NUL
reads an empty field, as 0 or as an error.

Decision point: whether a NUL before the digits of a size ends it.
Seen in: none of the scanned tarballs.
"""

VERDICT = "reject"
ID = "F41"
FEATURES = ["number.size.leading-nul"]


def build(a):
    a.header(b"a", b"0", b"\x000000001000\x00", note="a NUL, then 512 in octal")
    a.file(b"smuggled", b"", note="the data of a, to a reader that skips the NUL")
    a.end()

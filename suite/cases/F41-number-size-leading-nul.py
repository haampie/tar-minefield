"""A size with a NUL before its digits, which takes the next header for its data.

The archive has a file `a` whose size field starts with a NUL followed by `0000001000` and a NUL,
then an empty file `smuggled`.

In [POSIX][zero-filled], numeric fields are leading-zero-filled octal numbers [terminated][numeric]
by a space or a NUL. If a lenient reader skips the leading NUL, the size is octal 1000 (512) and the
next block is consumed as `a`'s data; if the reader stops at the first NUL, the size is 0 and the
next block is `smuggled`'s header.

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

"""A size with a plus sign, `+0000001000`.

The archive has a file `a` with `+0000001000` in its size field, followed by an empty file
`smuggled`.

In [POSIX][zero-filled], numeric fields are unsigned octal numbers filled with leading zeros. Read
leniently, a reader that skips the leading `+` reads octal 1000 (512) and consumes the next block as
`a`'s data. A reader that stops at the `+` reads a size of 0 and treats the next block as
`smuggled`'s header. A reader that takes a leading sign for the start of a base-64 number, as some
early test versions of GNU tar wrote them, decodes a huge size and consumes the rest of the archive
as `a`'s data.

Decision point: whether a numeric field may have a sign.
Seen in: none of the scanned tarballs.
See also: F23, a pax size with a plus sign, and F37, a size with the digit 9.
"""

VERDICT = "reject"
ID = "F51"
FEATURES = ["number.size.invalid-character"]


def build(a):
    a.header(b"a", b"0", b"+0000001000\0", note="size 512, or 0")
    a.file(b"smuggled", b"", note="the data of a, to an implementation that skips the sign")
    a.end()

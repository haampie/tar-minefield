"""A size with a plus sign, `+0000001000`.

The archive has a file `a`, whose size field is `+0000001000`, then an empty file `smuggled`.

In [POSIX][zero-filled], numeric fields are octal numbers filled with leading zeros, without a
sign. Read leniently, this case is ambiguous because the size is 512, which is octal 1000, if the
sign is skipped (and the next block is the data of `a`); 0, if the number ends at the sign (and the
next block is the header of `smuggled`); or a size far past the end of the archive, to a reader
that takes a sign for the start of a base-64 number, as some early test versions of GNU tar wrote
them (and the rest of the archive is the data of `a`).

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

"""A size with a space among its digits, which reads as two sizes.

The archive has a file `a`, whose size field is `000000 1000`, with a space among its digits, then
an empty file `smuggled`.

In [POSIX][numeric], a numeric field is octal digits terminated by spaces or NULs, and nothing
follows them. Read leniently, this case is ambiguous because the size is either 0, if the number
ends at the first blank (and the next block is the header of `smuggled`), or 1000 octal, 512, if the
blank is skipped (and the next block is the data of `a`).

Decision point: how a numeric field with a space among its digits is read.
Seen in: none of the scanned tarballs.
"""

VERDICT = "reject"
ID = "F12"
FEATURES = ['number.size.gap-in-digits']


def build(a):
    a.header(b"a", b"0", b"000000 1000\0", note="size 0 or 512")
    a.file(b"smuggled", b"", note="the data of a, to an implementation that skips spaces")
    a.end()

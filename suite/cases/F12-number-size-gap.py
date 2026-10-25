"""A size with a space among its digits, which reads as two sizes.

The size field is `000000 1000`. In POSIX, a numeric field is octal digits terminated by spaces or
NULs, and nothing follows them. Read leniently, this case is ambiguous because the size is either 0,
ending at the first blank, or 1000 octal, 512, with the blank skipped. The 512 bytes that follow are
then the header of `smuggled`, or the data of `a`.

Decision point: how a number field with a space among its digits is read.
Seen in: no source tarball.
"""

VERDICT = "reject"
ID = "F12"
FEATURES = ['number.size.gap-in-digits']


def build(a):
    a.header(b"a", b"0", b"000000 1000\0", note="size 0 or 512")
    a.file(b"smuggled", b"", note="the data of a, to an implementation that skips spaces")
    a.end()

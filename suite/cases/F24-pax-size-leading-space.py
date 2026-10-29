"""A pax `size` with a leading space, ` 512`, which conversions of strings to numbers skip.

The archive has a file `a`, whose pax header has the size ` 512`, with a space before it, and whose
header has the size 0, then an empty file `smuggled`.

A pax record is `<length> <key>=<value>\\n`, and its value starts right after the `=`: here, with a
space. In [POSIX][size-decimal], a pax size is decimal digits only, but Python's `int` and C's
`strtoull` skip leading whitespace, and read 512. Read leniently, this case is ambiguous because the
size is either 512, as read that way (and the next block is the data of `a`), or 0, as the header
specifies (and the next block is the header of `smuggled`). Neither is a reading of POSIX: ` 512` is
not a pax size, and the header's size is to be [ignored][corresponding] once a `size` record is
there.

Decision point: whether a pax size may have whitespace.
Seen in: none of the scanned tarballs.
"""

VERDICT = "reject"
ID = "F24"
FEATURES = ["pax.invalid-size"]


def build(a):
    a.pax([(b"size", b" 512")], note="size= 512, for a")
    a.header(b"a", b"0", 0, note="size 0")
    a.file(b"smuggled", b"", note="the data of a, to an implementation that skips the space")
    a.end()

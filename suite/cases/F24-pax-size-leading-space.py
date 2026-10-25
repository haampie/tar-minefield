"""A pax `size` with a leading space, ` 512`, which conversions of strings to numbers skip.

A pax record is `<length> <key>=<value>\\n`, and its value starts right after the `=`: here, with a
space. In POSIX, a pax size is decimal digits only, but Python's `int` and C's `strtoull` skip
leading whitespace, and read 512. Read leniently, this case is ambiguous because the size is either
that number, and the next block the data of `a`, or the header's, 0, and that block the header of
`smuggled`.

Decision point: whether a pax size may have whitespace.
Seen in: no source tarball.
"""

VERDICT = "reject"
ID = "F24"
FEATURES = ["pax.invalid-size"]


def build(a):
    a.pax([(b"size", b" 512")], note="size= 512, for a")
    a.header(b"a", b"0", 0, note="size 0")
    a.file(b"smuggled", b"", note="the data of a, to an implementation that skips the space")
    a.end()

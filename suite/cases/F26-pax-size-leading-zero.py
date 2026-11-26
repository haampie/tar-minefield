"""A pax `size` with a leading zero, `0777`: 777 in decimal, as POSIX says, or 511 in octal.

The archive has a file `a` with `size=0777` in its pax header and size 0 in its ustar header,
followed by two empty files, `smuggled-1` and `smuggled-2`.

A pax size is a [decimal number][size-decimal] and POSIX does not forbid leading zeros, so the
POSIX size is 777 bytes (spanning two 512-byte blocks and consuming both `smuggled-1` and
`smuggled-2` as `a`'s data). However, a reader that parses pax numbers with C's `strtoul(s, NULL,
0)` or treats leading-zero numbers as octal reads `0777` as 511 bytes (consuming one block, so
`smuggled-2` is extracted as a separate file). A reader that rejects the leading zero and falls back
to the ustar size of 0—contrary to POSIX, which requires [ignoring][corresponding] the ustar size—
extracts both `smuggled-1` and `smuggled-2`.

Decision point: whether a pax number with a leading zero is decimal or octal.
Seen in: none of the scanned tarballs.
"""

VERDICT = "reject"
ID = "F26"
FEATURES = ["pax.size-leading-zero"]


def build(a):
    a.pax([(b"size", b"0777")], note="size=0777, for a")
    a.header(b"a", b"0", 0, note="size 0")
    a.file(b"smuggled-1", b"", note="the data of a, to any reading of its pax size")
    a.file(b"smuggled-2", b"", note="the data of a, to a decimal reading of its pax size")
    a.end()

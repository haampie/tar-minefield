"""A pax `size` with a leading zero, `0777`: 777 in decimal, as POSIX says, or 511 in octal.

The archive has a file `a`, whose pax header has `size=0777` and whose header has the size 0, then
two empty files, `smuggled-1` and `smuggled-2`.

A pax size is decimal, and [POSIX][size-decimal] does not forbid leading zeros, so the size is 777.
But a reader that converts with C's `strtoul(s, NULL, 0)`, or that knows the header's octal numbers,
reads `0777` as octal, 511. This case is ambiguous in practice because the size is 777, in decimal,
511, in octal, or the header's, 0, with the pax size discarded. The data of `a` then takes two
blocks, one, after which `smuggled-2` is a member, or none, and both `smuggled-1` and `smuggled-2`
are.

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

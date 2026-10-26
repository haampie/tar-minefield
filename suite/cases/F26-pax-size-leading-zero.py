"""A pax `size` with a leading zero, `0777`: 777 in decimal, as POSIX says, or 511 in octal.

A pax size is decimal, and POSIX does not forbid leading zeros, so the size is 777. But a reader
that converts with C's `strtoul(s, NULL, 0)`, or that knows the header's octal numbers, reads `0777`
as octal, 511. This case is ambiguous in practice because BusyBox, PharData, RubyGems, Archive::Tar
and Haskell's tar take the header's size, 0, instead of 777, so that both `smuggled-1` and
`smuggled-2` are members. Read as octal, the data of `a` takes one block, and `smuggled-2` is a
member.

Decision point: whether a pax number with a leading zero is decimal or octal.
Seen in: none of the scanned tarballs.
"""

VERDICT = "reject"
ID = "F26"
FEATURES = ["pax.size-leading-zero"]
POSIX = "size-decimal"


def build(a):
    a.pax([(b"size", b"0777")], note="size=0777, for a")
    a.header(b"a", b"0", 0, note="size 0")
    a.file(b"smuggled-1", b"", note="the data of a, to any reading of its pax size")
    a.file(b"smuggled-2", b"", note="the data of a, to a decimal reading of its pax size")
    a.end()

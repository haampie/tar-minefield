"""A negative pax `size`, which a member cannot have.

The archive has a file `a`, whose pax header has `size=-512` and whose header has the size 0, then
an empty file `smuggled`.

In [POSIX][size-decimal], a pax size is decimal digits, without a sign. Read leniently, this case is
ambiguous because the size is either 0, as the header specifies (and the next block is the header of
`smuggled`), or the pax size read as an unsigned number, almost 2^64 (which runs past the end of the
archive). Neither is a reading of POSIX: `-512` is not a pax size, and the header's size is to be
[ignored][corresponding] once a `size` record is there.

Decision point: whether a pax size may be negative, and what a negative one means.
Seen in: none of the scanned tarballs.
"""

VERDICT = "reject"
ID = "F22"
FEATURES = ["pax.invalid-size"]


def build(a):
    a.pax([(b"size", b"-512")], note="size=-512, for a")
    a.header(b"a", b"0", 0, note="size 0")
    a.file(b"smuggled", b"", note="a member, unless a reading of the pax size covers it")
    a.end()

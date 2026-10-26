"""A negative pax `size`, which a member cannot have.

The pax header of `a` has `size=-512`, and the size field of its header is 0. In POSIX, a pax size
is decimal digits, without a sign. Read leniently, this case is ambiguous because the size is either
what the header specifies, 0 (and the next block is the header of `smuggled`), or the pax size read
as an unsigned number, almost 2^64 (which runs past the end of the archive). A reader may also
extract nothing at all, without an error.

Decision point: whether a pax size may be negative, and what a negative one means.
Seen in: none of the scanned tarballs.
"""

VERDICT = "reject"
ID = "F22"
FEATURES = ["pax.invalid-size"]
POSIX = "size-decimal"


def build(a):
    a.pax([(b"size", b"-512")], note="size=-512, for a")
    a.header(b"a", b"0", 0, note="size 0")
    a.file(b"smuggled", b"", note="a member, unless a reading of the pax size covers it")
    a.end()

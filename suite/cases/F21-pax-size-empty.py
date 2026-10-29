"""An empty pax `size`, which in POSIX removes the size rather than giving one.

The archive has a file `a`, whose header has the size 512 and whose pax header has an empty
`size=`, then an empty file `smuggled`.

[POSIX][empty-value] says that a record with an empty value deletes the field of that name, in the
header too, so `size=` technically leaves `a` without a size field, and the header's is to be
[ignored][corresponding]. But its order of precedence [assigns][x-assigned] the empty value, or,
[failing that][header-fallback], takes the header's size, 512. This case is ambiguous because the
size is then none, and the member is invalid, or 0, and the next block is the header of `smuggled`,
or 512, and the next block is the data of `a`.

Decision point: what an empty pax size means: no size, a size of 0, or the header's size.
Seen in: none of the scanned tarballs.
"""

VERDICT = "reject"
ID = "F21"
FEATURES = ["pax.empty-value.size", "pax.invalid-size"]


def build(a):
    a.pax([(b"size", b"")], note="size=, which removes the size")
    a.header(b"a", b"0", 512, note="size 512")
    a.file(b"smuggled", b"", note="the data of a, to an implementation that takes the header's size")
    a.end()

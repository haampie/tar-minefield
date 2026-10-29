"""An empty pax `size`, which in POSIX removes the size rather than giving one.

POSIX says that a record with an empty value deletes the field of that name, in the header too, so
`size=` leaves `a` with no size at all, not even the 512 of its header. It does not say what a
member without a size is. Nor does the header's size stand in, as a header field that a keyword
deletes is to be ignored. This case is ambiguous because the size is then either 0, and the next
block is the header of `smuggled`, or none, and the member is invalid. Readers also fall back to
what the header specifies, against POSIX, and the next block is the data of `a`.

Decision point: what an empty pax size means: no size, 0, or the header's size.
Seen in: none of the scanned tarballs.
"""

VERDICT = "reject"
ID = "F21"
FEATURES = ["pax.empty-value.size", "pax.invalid-size"]
POSIX = {"POSIX": "empty-value", "ignored": "corresponding"}


def build(a):
    a.pax([(b"size", b"")], note="size=, which removes the size")
    a.header(b"a", b"0", 512, note="size 512")
    a.file(b"smuggled", b"", note="the data of a, to an implementation that takes the header's size")
    a.end()

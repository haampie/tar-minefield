"""An empty pax `size`, which in POSIX removes the size rather than giving one.

The archive has a file `a` with size 512 in its ustar header and an empty `size=` record in its pax
header, followed by an empty file `smuggled`.

Under [POSIX][empty-value], an empty pax value deletes the corresponding attribute, including the
ustar field, which is then [ignored][corresponding]—leaving `a` with no size at all. On the other
hand, the POSIX precedence rules say to [assign][x-assigned] the pax value or [fall back to the
ustar header][header-fallback] (512). Depending on how a reader resolves `size=`, it either rejects
`a` for having no size, treats the empty string as 0 and extracts `smuggled`, or falls back to the
ustar size of 512 and consumes `smuggled`'s header as `a`'s data.

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

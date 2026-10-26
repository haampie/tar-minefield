"""A pax `size` that disagrees with the header's size, which hides a header from one implementation.

The size field in the header of `a` is 512, and its pax extended header has `size=0`. POSIX says
that the pax size overrides the header's: it is how sizes over 8 GiB, which do not fit in the
header's size field, are written, and archivers write various sizes in the header then. An
implementation that takes the pax size, as it must, reads the next block as the header of another
file, `smuggled`; an implementation that takes the header's size, or does not know pax, reads that
block as the data of `a`. An implementation that takes the header's size is the bug of
CVE-2025-62518 (tokio-tar). A strict parser may reject a header whose size field has room for the
size but gives another, but must not extract `a` with 512 bytes.

Decision point: which of two sizes frames the member.
Seen in: none of the scanned tarballs.
"""

VERDICT = "tolerate"
ID = "F14"
FEATURES = ["pax.size-disagrees"]
POSIX = "size-override"
TREE = [
    {"path": "a", "kind": "file", "contents": b"", "executable": False},
    {"path": "smuggled", "kind": "file", "contents": b"", "executable": False},
]


def build(a):
    a.pax([(b"size", b"0")], note="size=0, for a")
    a.header(b"a", b"0", 512, note="size 512")
    a.file(b"smuggled", b"",
           note="the data of a, to an implementation that takes the header's size")
    a.end()

"""A pax `size` on a hard link, which takes the next header for its data.

The archive has a file `a`, then a hard link `h` to `a`, whose pax header has `size=512`, then an
empty file `smuggled`.

[POSIX][link-data] permits data on a hard link in pax, which its `x` header suggests, so the next
block is the data of `h`, but does not say what that data does: whether it replaces the contents of
`a`, or is ignored. A reader that reads it as ustar, in which [no data][no-data] is stored for a
hard link, reads the block as the header of a file, `smuggled`; the bytes do not say which it is.
This case is ambiguous because the tree has `a` as it is, `a` with that block as its contents, or
`a` and `smuggled`.

Decision point: whether a pax size applies to a hard link.
Seen in: none of the scanned tarballs.
See also: F15, a pax size on a directory, and F34, a size in the header of a hard link.
"""

VERDICT = "reject"
ID = "F35"
FEATURES = ["pax.size-on-hardlink"]


def build(a):
    a.file(b"a", b"a\n")
    a.pax([(b"size", b"512")], note="for h")
    a.hardlink(b"h", b"a", note="a hard link to a, but the pax size is 512")
    a.file(b"smuggled", b"", note="the block that the pax size covers")
    a.end()

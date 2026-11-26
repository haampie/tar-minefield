"""A pax `size` on a hardlink, which takes the next header for its data.

The archive has a file `a`, a hardlink `h` to `a` with `size=512` in its pax header, and an empty
file `smuggled`.

In the pax format (indicated by `h`'s `x` header), hardlinks [may carry data blocks][link-data], so
the block after `h` is its data—though POSIX leaves unspecified whether hardlink data replaces `a`'s
contents or is ignored. A reader that applies the ustar rule, where [no data is stored][no-data] for
hardlinks, reads that block as `smuggled`'s header instead. Depending on the reader, the extracted
tree has `a` with its original contents, `a` overwritten with the 512-byte block, or `a` and
`smuggled`.

Decision point: whether a pax size applies to a hardlink.
Seen in: none of the scanned tarballs.
See also: F15, a pax size on a directory, and F34, a size in the header of a hardlink.
"""

VERDICT = "reject"
ID = "F35"
FEATURES = ["pax.size-on-hardlink"]


def build(a):
    a.file(b"a", b"a\n")
    a.pax([(b"size", b"512")], note="for h")
    a.hardlink(b"h", b"a", note="a hardlink to a, but the pax size is 512")
    a.file(b"smuggled", b"", note="the block that the pax size covers")
    a.end()

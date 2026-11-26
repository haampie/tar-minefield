r"""A size in the header of a hardlink, in a pax archive, which takes the next header for its data.

The archive has a file `a`, a hardlink `h` to `a` preceded by a pax header and carrying size 512 in
its ustar header, and an empty file `smuggled`.

In the pax format (indicated by `h`'s `x` header), hardlinks [may carry data blocks][link-data],
making the block after `h` its data rather than `smuggled`'s header—though POSIX does not specify
whether hardlink data overwrites `a` or is ignored. A reader that instead follows the ustar rule,
where [no data is stored][no-data] for hardlinks, treats the next block as `smuggled`'s header.
Depending on the reader, the extracted tree has `a` and `h` (containing either `a\n` or the 512-byte
block), or `a`, `h` and `smuggled`.

Decision point: whether a size in the header of a hardlink applies, in an archive with pax headers.
Seen in: none of the scanned tarballs.
See also: F33, a size in the header of a directory, F35, a pax size on a hardlink, and F38, the same
in an archive without pax headers.
"""

VERDICT = "reject"
ID = "F34"
FEATURES = ["size.on-hardlink"]


def build(a):
    a.file(b"a", b"a\n")
    a.pax([(b"mtime", b"1")], note="for h, which makes the archive pax")
    a.header(b"h", b"1", 512, note="a hardlink to a, with a size of 512", linkname=b"a")
    a.file(b"smuggled", b"", note="the block that the size covers")
    a.end()

"""A size in the header of a hard link, in a pax archive, which takes the next header for its data.

The first member is a file `a`, the second a hard link `h` to `a`, with a pax extended header and
the size 512 in its ustar header. In a pax archive, which this is, POSIX permits data on a hard
link, so the block after the header of `h` is its data, and what looks like the header of `smuggled`
is that data. POSIX does not say what the data of a hard link does: whether it replaces the contents
of `a`, or is ignored. A reader that applies the rule of ustar, that no data is stored for a hard
link, reads `smuggled` as a member. This case is ambiguous because the tree has `a` as it is, `a`
with that block as its contents, or `a` and `smuggled`. A reader may also make `h` a file of the
block.

Decision point: whether a size in the header of a hard link applies, in an archive with pax headers.
Seen in: none of the scanned tarballs.
See also: F33, a size in the header of a directory, and F35, a pax size on a hard link.
"""

VERDICT = "reject"
ID = "F34"
FEATURES = ["size.on-hardlink"]
POSIX = {"POSIX": "link-data", "rule of ustar": "no-data"}


def build(a):
    a.file(b"a", b"a\n")
    a.pax([(b"mtime", b"1")], note="for h, which makes the archive pax")
    a.header(b"h", b"1", 512, note="a hard link to a, with a size of 512", linkname=b"a")
    a.file(b"smuggled", b"", note="the block that the size covers")
    a.end()

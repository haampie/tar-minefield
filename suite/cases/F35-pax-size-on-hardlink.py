"""A pax `size` on a hard link, which takes the next header for its data.

The first member is a file `a`, the second a hard link `h` to `a`, whose pax extended header has
`size=512`. POSIX says that no data is stored for a hard link in ustar, but permits it in pax. This
case is ambiguous because the next block is either the header of a file, `smuggled`, or the data of
`h`, which replaces the contents of `a`, as libarchive reads it.

Decision point: whether a pax size applies to a hard link.
Seen in: none of the scanned tarballs.
See also: F15, a pax size on a directory, and F34, a size in the header of a hard link.
"""

VERDICT = "reject"
ID = "F35"
FEATURES = ["pax.size-on-hardlink"]
POSIX = {"POSIX": "no-data", "permits": "link-data"}


def build(a):
    a.file(b"a", b"a\n")
    a.pax([(b"size", b"512")], note="for h")
    a.hardlink(b"h", b"a", note="a hard link to a, but the pax size is 512")
    a.file(b"smuggled", b"", note="the block that the pax size covers")
    a.end()

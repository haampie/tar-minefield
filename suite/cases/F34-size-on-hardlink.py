"""A size in the header of a hard link, in a pax archive, which takes the next header for its data.

The first member is a file `a`, the second a hard link `h` to `a`, with a pax extended header and
the size 512 in its ustar header. POSIX says that no data is stored for a hard link in ustar, so the
next block is the header of a file, `smuggled`. It permits data on a hard link in pax, and
libarchive reads it once an archive has a pax header: the block is then the data of `h`, which
replaces the contents of `a`. This case is ambiguous because the tree has either `a` as it is and
`smuggled`, or `a` with that block as its contents.

Decision point: whether a size in the header of a hard link applies, in an archive with pax headers.
Seen in: no source tarball.
See also: F33, a size in the header of a directory, and F35, a pax size on a hard link.
"""

VERDICT = "reject"
ID = "F34"
FEATURES = ["size.on-hardlink"]
POSIX = {"POSIX": "no-data", "permits": "link-data"}


def build(a):
    a.file(b"a", b"a\n")
    a.pax([(b"mtime", b"1")], note="for h, which makes the archive pax")
    a.header(b"h", b"1", 512, note="a hard link to a, with a size of 512", linkname=b"a")
    a.file(b"smuggled", b"", note="the block that the size covers")
    a.end()

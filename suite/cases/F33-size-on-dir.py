"""A size in the header of a directory, which takes the next header for its data.

The ustar header of a directory says 512 bytes. In POSIX, no data is stored for a directory,
whatever its size, so the next block is the header of a file, `smuggled`. This case is ambiguous in
practice because, if the size applies, that block is the directory's data instead, and the tree is a
directory alone. The same goes for links and devices, which have no data either.

Decision point: whether a size in the header applies to a member that has no data.
Seen in: no source tarball has a size on a member without data.
See also: F15, a pax `size` on a directory, which is rejected as well.
"""

VERDICT = "reject"
ID = "F33"
FEATURES = ["size.on-dir"]


def build(a):
    a.header(b"dir/", b"5", 512, note="no data, but the size says 512 bytes")
    a.file(b"dir/smuggled", b"", note="the block that the size covers")
    a.end()

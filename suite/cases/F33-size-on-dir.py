"""A size in the header of a directory, which takes the next header for its data.

The archive has a directory `dir/`, whose size field is 512, then an empty file `dir/smuggled`.

In [POSIX][no-data], no data is stored for a directory, whatever its size, so the next block is the
header of a file, `dir/smuggled`. This case is ambiguous in practice because, if the size applies,
that block is the directory's data instead, and the tree is a directory alone. The same goes for
symlinks and devices, which do not have data either, and implementations need not decide alike for
every kind: one that skips the size of a directory may take the size of a symlink for its data.

Decision point: whether a size in the header applies to a member without data.
Seen in: none of the scanned tarballs.
See also: F15, a pax `size` on a directory, and F34, a size in the header of a hard link, which
are rejected as well.
"""

VERDICT = "reject"
ID = "F33"
FEATURES = ["size.on-dir"]


def build(a):
    a.header(b"dir/", b"5", 512, note="no data, but its size field is 512")
    a.file(b"dir/smuggled", b"", note="the block that the size covers")
    a.end()

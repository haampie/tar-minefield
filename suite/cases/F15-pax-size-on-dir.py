"""A pax `size` on a directory, which takes the next header for its data.

The archive has a directory `dir/`, whose pax header has `size=512`, then an empty file
`dir/smuggled`.

In [POSIX][no-data], no data is stored for a directory, whatever its size, so the next block is the
header of a file, `dir/smuggled`. This case is ambiguous in practice because, if the size applies,
that block is the directory's data instead, and the tree is a directory alone.

Decision point: whether a pax `size` applies to a member without data.
Seen in: llama_index_workflows 2.26.0, with a pax size on a directory.
See also: F33, a size in the ustar header of a directory, and F35, a pax `size` on a hard link,
which are rejected as well.
"""

VERDICT = "reject"
ID = "F15"
FEATURES = ["pax.size-on-dir"]


def build(a):
    a.pax([(b"size", b"512")], note="for dir/, with size=512")
    a.directory(b"dir/", note="no data, but the pax size is 512")
    a.file(b"dir/smuggled", b"", note="the block that the pax size covers")
    a.end()

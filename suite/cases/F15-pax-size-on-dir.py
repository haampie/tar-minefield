"""A pax `size` on a directory, which takes the next header for its data.

The archive has a directory `dir/` with `size=512` in its pax header, followed by an empty file
`dir/smuggled`.

Under [POSIX][no-data], directories do not store data blocks regardless of size, so the next block
is `dir/smuggled`'s header. A reader that honors `size=512` on a directory consumes that block as
the directory's data and extracts only `dir/`.

Decision point: whether a pax `size` applies to a member without data.
Seen in: llama_index_workflows 2.26.0, with a pax size on a directory.
See also: F33, a size in the ustar header of a directory, and F35, a pax `size` on a hardlink, which
are rejected as well.
"""

VERDICT = "reject"
ID = "F15"
FEATURES = ["pax.size-on-dir"]


def build(a):
    a.pax([(b"size", b"512")], note="for dir/, with size=512")
    a.directory(b"dir/", note="no data, but the pax size is 512")
    a.file(b"dir/smuggled", b"", note="the block that the pax size covers")
    a.end()

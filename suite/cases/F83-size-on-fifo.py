"""A size in the header of a FIFO, which takes the next header for its data.

The archive has a FIFO `p`, of typeflag `6`, whose size field is 512, then an empty file `smuggled`,
then a file `b`.

In [POSIX][special-no-data], an archive does not store data for a FIFO or a device, and the size of
a FIFO is [ignored][fifo-size] by a reader, so the next block is the header of `smuggled`. For a
device, it is not specified whether a reader ignores the size. This case is ambiguous in practice
because a reader that ignores the size extracts `smuggled` and `b`, and one that skips 512 bytes of
data, or extracts them as the contents of a file `p`, extracts `b` without `smuggled`.

Decision point: whether the size in the header of a FIFO applies.
Seen in: none of the scanned tarballs.
See also: F68, a size in the header of a symlink, and K08, a FIFO.
"""

VERDICT = "reject"
ID = "F83"
FEATURES = ["size.on-fifo"]


def build(a):
    a.header(b"p", b"6", 512, note="a FIFO, which has no data, but its size field is 512")
    a.file(b"smuggled", b"", note="the block that the size covers")
    a.file(b"b", b"b\n")
    a.end()

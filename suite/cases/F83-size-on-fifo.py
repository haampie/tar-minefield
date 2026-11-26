"""A non-zero size in a FIFO header, covering the next member's header.

The archive has a FIFO `p` (typeflag `6`) with a size field of 512, followed by an empty file
`smuggled` and a file `b`.

Under [POSIX][special-no-data], archives do not store data blocks for FIFOs or device nodes, and
readers [must ignore][fifo-size] a FIFO's size field (for devices, POSIX leaves the size field's
effect unspecified). The block after `p` is therefore `smuggled`'s header. A reader that ignores the
FIFO's size reaches `smuggled` and `b`, whereas one that skips 512 bytes of data, or extracts `p` as
a regular file containing those 512 bytes, consumes `smuggled`'s header and extracts `b` without
`smuggled`.

Decision point: whether a non-zero size in a FIFO header consumes data blocks.
Seen in: none of the scanned tarballs.
See also: F68, a non-zero size on a symlink, and K08, a FIFO.
"""

VERDICT = "reject"
ID = "F83"
FEATURES = ["size.on-fifo"]


def build(a):
    a.header(b"p", b"6", 512, note="FIFO with size 512")
    a.file(b"smuggled", b"", note="covered by p's size")
    a.file(b"b", b"b\n")
    a.end()

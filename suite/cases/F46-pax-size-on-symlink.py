"""A symlink with a pax `size`: data to skip, or none?

The archive has a symlink `l` to `target`, whose pax header has `size=512` and whose header has the
size 0, then an empty file `smuggled`, then a file `b`.

In POSIX, a pax `size` [overrides][size-override] the size field of the header, but [no
data][no-data] is stored for a symlink, whose size field [is zero][link-size-zero]. This case is
ambiguous because the next block is either the data of `l`, 512 bytes to skip, or the header of
`smuggled`, which is then a member of its own.

Decision point: whether a pax size applies to a member that has no data.
Seen in: none of the scanned tarballs.
See also: F15, a pax size on a directory, and F35, a pax size on a hardlink.
"""

VERDICT = "reject"
ID = "F46"
FEATURES = ["pax.size-on-symlink"]


def build(a):
    a.pax([(b"size", b"512")], note="size=512, for l")
    a.symlink(b"l", b"target", note="size 0")
    a.file(b"smuggled", b"", note="the data of l, to an implementation that applies the pax size")
    a.file(b"b", b"b\n")
    a.end()

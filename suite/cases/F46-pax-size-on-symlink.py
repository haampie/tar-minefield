"""A symlink with a pax `size`: data to skip, or none?

The archive has a symlink `l` to `target` with `size=512` in its pax header and size 0 in its ustar
header, followed by an empty file `smuggled` and a file `b`.

In POSIX, a pax `size` [overrides][size-override] the ustar size field, yet symlinks [do not store
data][no-data] and their size field [must be zero][link-size-zero]. A reader that honors `size=512`
on the symlink skips the next block as `l`'s data and misses `smuggled`, whereas one that ignores
sizes on symlinks reads the next block as `smuggled`'s header.

Decision point: whether a pax size applies to a member that does not have data.
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

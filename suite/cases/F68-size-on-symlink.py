"""A size in the header of a symlink, which takes the next header for its data.

The archive has a symlink `l` to `target`, whose size field is 512, then an empty file `smuggled`,
then a file `b`.

In [POSIX][no-data], an archive does not store data for a symlink, and its size is [specified as
zero][link-size-zero], so the next block is the header of `smuggled`. This case is ambiguous in
practice because a reader can take the size in one of four ways. A reader that ignores it extracts
the link, `smuggled` and `b`. One that skips 512 bytes of data extracts the link and `b`. One that
reads the data as the target of the link extracts a link to `smuggled`, which is the string at the
start of that block. One that extracts a symlink as a file writes that block as its contents. Other
readers report an error.

Decision point: whether the size in the header of a symlink applies.
Seen in: none of the scanned tarballs.
See also: F46, a pax `size` on a symlink, and F34, a size in the header of a hardlink.
"""

VERDICT = "reject"
ID = "F68"
FEATURES = ["size.on-symlink"]


def build(a):
    a.header(b"l", b"2", 512, linkname=b"target", note="no data, but its size field is 512")
    a.file(b"smuggled", b"", note="the block that the size covers")
    a.file(b"b", b"b\n")
    a.end()

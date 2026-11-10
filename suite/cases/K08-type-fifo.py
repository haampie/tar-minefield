"""A FIFO: created, an empty file, or left out?

The archive has a FIFO `p`, of typeflag `6`, then a file `b`.

In POSIX, typeflag `6` is a FIFO, of which an archive has [the existence][fifo], and not contents. A
reader that cannot create one has an [error][cannot-create]: only a type that can have data is
[extracted as a regular file][unknown-type] instead. A tree of files, directories and links does not
have a place for a FIFO. This case is ambiguous in practice because a reader can take the member in
one of four ways. A reader that supports FIFOs creates one. One that extracts every member that is
not a directory or a link as a file creates an empty file `p`. One that skips the kinds of members
that it does not extract leaves `p` out, without an error. Other readers report an error.

Decision point: what a reader makes of a member that is not a file, a directory or a link.
Seen in: not measured as a feature, but the scans record the kinds of members: one tarball, forktty
1.3, has a FIFO, and none has a device.
See also: F16, an unknown typeflag.
"""

VERDICT = "reject"
ID = "K08"
FEATURES = ["type.fifo"]


def build(a):
    a.header(b"p", b"6", 0, note="a FIFO")
    a.file(b"b", b"b\n")
    a.end()

"""A FIFO: created, an empty file, or skipped?

The archive has a FIFO `p`, of typeflag `6`, then a file `b`.

In POSIX, typeflag `6` is a FIFO, a member [without contents][fifo]. A FIFO that cannot be created
is an [error][cannot-create]: only a type that can have data is [extracted as a regular
file][unknown-type] instead. A FIFO is not part of the tree, which has files, directories and links.
This case is ambiguous in practice because a reader can take the member in one of four ways. A
reader that supports FIFOs creates one. One that extracts every member that is not a directory or a
link as a file extracts an empty file `p`. One that skips the kinds of members that it does not
extract extracts `b` alone, without an error. Other readers report an error.

Decision point: what a reader does with a member that is not a file, a directory or a link.
Seen in: not measured, as earlier versions of the scanner did not have a feature for it: the scans
did record the kinds of members, and one tarball, forktty 1.3, has a FIFO.
See also: F16, an unknown typeflag.
"""

VERDICT = "reject"
ID = "K08"
FEATURES = ["type.fifo"]


def build(a):
    a.header(b"p", b"6", 0, note="a FIFO")
    a.file(b"b", b"b\n")
    a.end()

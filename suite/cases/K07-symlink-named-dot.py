"""A symlink named `.`: the root of the tree replaced by a link, or dropped?

The archive has a directory `d`, then a symlink `.` to `d`, then a file `f`.

The special filename [dot][dot] refers to the directory that it is in, so in [POSIX][resolution] a
member named `.` is the directory that the archive is extracted to. Creating a symlink there fails,
as [the name exists][symlink-exists], which is an [error][cannot-create]. This case is ambiguous in
practice because the symlink is dropped, as a name that normalizes to the root, and the tree is `d`
and `f`, or is created under another name, such as `_`, or the member is an error.

Decision point: whether a link may be named `.`.
Seen in: not measured: 64 of the scanned tarballs have a member named `.` or `./`, and the scans
did not record its kind.
See also: N05, a directory named `./`.
"""

VERDICT = "reject"
ID = "K07"
FEATURES = ["name.dot-on-symlink"]


def build(a):
    a.directory(b"d")
    a.symlink(b".", b"d", note="a symlink named .")
    a.file(b"f", b"f\n")
    a.end()

"""A symlink `.`: dropped, renamed, or an error?

The archive has a directory `d`, then a symlink `.` to `d`, then a file `f`.

The special filename [dot][dot] refers to the directory that it is in, so in [POSIX][resolution] a
member `.` is the directory that the archive is extracted to. Creating a symlink there fails, as
[the name exists][symlink-exists], which is an [error][cannot-create]. This case is ambiguous in
practice because a reader can take the symlink in one of three ways. A reader that normalizes the
name to the root drops the symlink, and extracts `d` and `f`. One that renames the member creates
the symlink under another name, such as `_`. Other readers report an error.

Decision point: whether a link may have the name `.`.
Seen in: not measured, as the scans did not record the kind of a member `.`: 64 of the scanned
tarballs have a member `.` or `./`.
See also: N05, a directory `./`.
"""

VERDICT = "reject"
ID = "K06"
FEATURES = ["name.dot-on-symlink"]


def build(a):
    a.directory(b"d")
    a.symlink(b".", b"d", note="a symlink named .")
    a.file(b"f", b"f\n")
    a.end()

"""A symlink `.`: dropped, renamed, or an error?

The archive has a directory `d`, a symlink `.` to `d`, and a file `f`.

The special filename [dot][dot] refers to the directory that it is in, so in [POSIX][resolution] a
member `.` is the destination directory itself. Creating a symlink at an [existing
path][symlink-exists] fails and is an [error][cannot-create]. A reader that normalizes `.` to the
root and skips it extracts `d` and `f`. A reader that sanitizes reserved names creates the symlink
under a substitute name such as `_`, while others report an error.

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

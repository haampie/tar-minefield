"""A regular file `.`: dropped, renamed, or an error?

The archive has a regular file `.`, then a file `b`.

The special filename [dot][dot] refers to the directory that it is in, so in [POSIX][resolution] a
member `.` is the directory that the archive is extracted to. A file cannot be created at that path,
which is an [error][cannot-create]. This case is ambiguous in practice because a reader can take the
member in one of three ways. A reader that normalizes the name to the root, or skips a member whose
name it cannot use, drops the file, and extracts `b` without an error. One that renames the member
creates the file under another name, such as `_`. Other readers report an error.

Decision point: whether a file may have the name `.`.
Seen in: not measured, as the scans did not record the kind of a member `.`: 64 of the scanned
tarballs have a member `.` or `./`.
See also: K06, a symlink `.`, and N05, a directory `./`.
"""

VERDICT = "reject"
ID = "K14"
FEATURES = ["name.dot-on-file"]


def build(a):
    a.file(b".", b"a file named .\n", note="a file named .")
    a.file(b"b", b"b\n")
    a.end()

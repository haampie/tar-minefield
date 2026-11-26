"""A regular file named `.`: skipped, renamed, or an error?

The archive has a regular file named `.`, followed by a file `b`.

Because [dot][dot] refers to the current directory, [POSIX][resolution] resolves `.` to the
destination directory itself. A regular file cannot be created over that directory, making this an
[error][cannot-create]. A reader that normalizes `.` away or skips uncreatable paths drops the first
member and extracts only `b`. A reader that sanitizes reserved names extracts the file under a
substitute name such as `_`, while others report an error.

Decision point: how a reader handles a regular file named `.`.
Seen in: not measured, as the scanner did not record the member kind of `.`; 64 scanned tarballs
contain a member named `.` or `./`.
See also: K06, a symlink named `.`, and N05, a directory `./`.
"""

VERDICT = "reject"
ID = "K14"
FEATURES = ["name.dot-on-file"]


def build(a):
    a.file(b".", b"a file named .\n", note="regular file named .")
    a.file(b"b", b"b\n")
    a.end()

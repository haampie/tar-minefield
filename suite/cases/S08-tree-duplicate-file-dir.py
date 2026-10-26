"""A file, then a directory of the same name.

The first member is a file `a`, the second a directory `a/`. POSIX says that a member is extracted
as a file of its own type, and permits a later member to overwrite an earlier one of the same name,
but does not require it. This case is ambiguous because the tree has either the directory, which
replaces the file, or the file, or neither.

Decision point: whether a later member replaces an earlier one of another kind.
Seen in: none of the scanned tarballs.
"""

VERDICT = "reject"
ID = "S08"
FEATURES = ['tree.duplicate.file-dir']
POSIX = {"POSIX": "file-type", "permits": "overwrite"}


def build(a):
    a.file(b"a", b"a file first\n")
    a.directory(b"a/")
    a.end()

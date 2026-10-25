"""A file, then a directory of the same name.

The first member is a file `a`, the second a directory `a/`. POSIX does not say what a later member
of another kind does to an earlier one. This case is ambiguous because the tree has either the
directory, which replaces the file, or the file.

Decision point: whether a later member replaces an earlier one of another kind.
Seen in: no source tarball.
"""

VERDICT = "reject"
ID = "S08"
FEATURES = ['tree.duplicate.file-dir']


def build(a):
    a.file(b"a", b"a file first\n")
    a.directory(b"a/")
    a.end()

"""A file, then a directory of the same name.

The archive has a file `a`, then a directory `a/`.

[POSIX][file-type] says that a member is extracted as a file of its own type, and that existing
files are [overwritten][overwritten] only when its options allow it, but not whether overwriting a
file includes replacing it with a directory. This case is ambiguous because the tree has either the
directory, which replaces the file, or the file, with an error for the directory.

Decision point: whether a later member replaces an earlier one of another kind.
Seen in: none of the scanned tarballs.
"""

VERDICT = "reject"
ID = "S08"
FEATURES = ['tree.duplicate.file-dir']


def build(a):
    a.file(b"a", b"a file first\n")
    a.directory(b"a/")
    a.end()

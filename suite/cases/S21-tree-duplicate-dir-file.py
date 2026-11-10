"""An empty directory, then a file of the same name.

The archive has a directory `a/`, then a file `a`.

In [POSIX][file-type], a member is extracted as a file of its own type, and existing files [can be
overwritten][overwritten], but it is not specified whether overwriting includes replacing a
directory with a file. An empty directory can be removed without losing anything. This case is
ambiguous because the tree has either the file, which replaces the directory, or the directory, with
an error for the file or without one.

Decision point: whether a later member replaces an earlier one of another kind.
Seen in: none of the scanned tarballs has a file at the path of a directory that is a member.
See also: S08, a file, then a directory of the same name, and S20, a file at the path of a directory
that has contents.
"""

VERDICT = "reject"
ID = "S21"
FEATURES = ["tree.duplicate.dir-file"]


def build(a):
    a.directory(b"a/")
    a.file(b"a", b"a file, after a directory\n")
    a.end()

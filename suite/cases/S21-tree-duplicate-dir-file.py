"""An empty directory followed by a regular file of the same name.

The archive has a directory `a/`, followed by a regular file `a`.

In [POSIX][file-type], each member is extracted with its archived file type and existing files [may
be overwritten][overwritten], but POSIX does not specify whether a regular file can replace an
existing directory. Although removing an empty directory does not lose any extracted files, readers
disagree on the result: a reader that removes the empty directory extracts the file `a`, whereas one
that refuses to replace a directory leaves `a/` in place (either reporting an error or skipping the
file).

Decision point: whether a regular file replaces an earlier empty directory.
Seen in: none of the scanned tarballs has a file at the path of an explicit directory member.
See also: S08, a file followed by a directory of the same name, and S20, a file at the path of a
non-empty directory.
"""

VERDICT = "reject"
ID = "S21"
FEATURES = ["tree.duplicate.dir-file"]


def build(a):
    a.directory(b"a/")
    a.file(b"a", b"a file, after a directory\n")
    a.end()

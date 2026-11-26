"""A file, then a directory of the same name.

The archive has a file `a`, followed by a directory `a/`.

In [POSIX][file-type], each member is extracted with its archived file type and existing files [may
be overwritten][overwritten], but POSIX does not specify whether a directory can replace an existing
regular file. A reader that removes the file extracts the directory `a/`, whereas one that refuses
to replace a file with a directory leaves the file `a` in place (or reports an error).

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

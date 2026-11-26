"""A file inside an implicit directory, followed by a regular file at that directory's path.

The archive has a file `a/f`, followed by a file `a`, with no directory member for `a`.

Extracting `a/f` requires [creating the parent directory][intermediate] `a`. The next member is a
regular file at the same path `a`. In [POSIX][file-type], each member is extracted with its archived
file type and existing files [may be overwritten][overwritten], but POSIX does not say whether a
regular file can replace a non-empty directory. A reader that removes the directory to extract the
file leaves only the file `a`, losing `a/f`. A reader that keeps the directory and ignores the
conflicting file leaves `a/f`, while other readers report an error.

Decision point: whether a regular file replaces a non-empty directory.
Seen in: not measured, as earlier scanner versions only compared explicit member names, and `a` is
an implicit directory.
See also: S08, a file followed by a directory of the same name, and S12, a member under a regular
file.
"""

VERDICT = "reject"
ID = "S20"
FEATURES = ["tree.duplicate.dir-file"]


def build(a):
    a.file(b"a/f", b"f\n", note="creates parent directory a")
    a.file(b"a", b"a\n", note="regular file at directory path a")
    a.end()

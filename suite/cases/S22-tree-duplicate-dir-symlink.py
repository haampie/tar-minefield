"""An empty directory followed by a symlink of the same name: replaced, kept, or placed inside?

The archive has a file `b`, a directory `a/`, and a symlink `a` to `b`.

In [POSIX][file-type], each member is extracted with its archived file type, and `symlink()` [fails
if the destination path already exists][symlink-exists]. A reader that removes the empty directory
before creating the symlink extracts `a` as a symlink. A reader that keeps the directory and skips
the symlink leaves `a/` and `b`. A reader that places the symlink inside an existing directory of
the same name, as `ln -s b a` does, creates `a/b`. Other readers report an error.

Decision point: how a reader handles a symlink at the path of an existing directory.
Seen in: none of the scanned tarballs has a symlink at the path of an explicit directory member.
See also: S14, a symlink followed by a directory of the same name, and S21, an empty directory
followed by a regular file.
"""

VERDICT = "reject"
ID = "S22"
FEATURES = ["tree.duplicate.dir-symlink"]


def build(a):
    a.file(b"b", b"b\n")
    a.directory(b"a/")
    a.symlink(b"a", b"b", note="symlink at directory path a")
    a.end()

"""An empty directory, then a symlink of the same name: replaced, kept, or the link inside it?

The archive has a file `b`, a directory `a/`, then a symlink `a` to `b`.

In [POSIX][file-type], a member is extracted as a file of its own type, and creating a symlink at a
path that exists [fails][symlink-exists]. This case is ambiguous because a reader can take the
symlink in one of four ways. A reader that replaces the directory extracts the link `a`. One that
keeps the directory extracts it and `b` alone, without an error. One that makes the link inside a
directory that is at its path, as `ln -s b a` does, extracts a link `a/b`. Other readers report an
error.

Decision point: whether a symlink replaces a directory.
Seen in: none of the scanned tarballs has a symlink at the path of a directory that is a member.
See also: S14, a symlink, then a directory of the same name, and S21, an empty directory, then a
file.
"""

VERDICT = "reject"
ID = "S22"
FEATURES = ["tree.duplicate.dir-symlink"]


def build(a):
    a.file(b"b", b"b\n")
    a.directory(b"a/")
    a.symlink(b"a", b"b", note="a symlink, after a directory")
    a.end()

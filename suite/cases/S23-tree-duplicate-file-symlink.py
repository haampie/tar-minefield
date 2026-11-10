"""A file, then a symlink of the same name.

The archive has a file `t`, a file `a`, then a symlink `a` to `t`.

In POSIX, existing files [can be overwritten][overwritten], but creating a symlink at a path that
exists [fails][symlink-exists], so a reader that extracts the link replaces the file. This case is
ambiguous because the tree has either the link, which replaces the file, or the file, with an error
for the link or without one.

Decision point: whether a later member replaces an earlier one of another kind.
Seen in: none of the scanned tarballs.
See also: S10, a symlink, then a file of the same name.
"""

VERDICT = "reject"
ID = "S23"
FEATURES = ["tree.duplicate.file-symlink"]


def build(a):
    a.file(b"t", b"t\n")
    a.file(b"a", b"a file first\n")
    a.symlink(b"a", b"t", note="a symlink, after a file")
    a.end()

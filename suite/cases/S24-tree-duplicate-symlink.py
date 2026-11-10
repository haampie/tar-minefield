"""The same symlink twice, with different targets: the first, or the last?

The archive has the files `first` and `second`, a symlink `a` to `first`, then a symlink `a` to
`second`.

In POSIX, a reader may [overwrite][overwrite] a file when an archive has several members of one
name, but creating a symlink at a path that exists [fails][symlink-exists], so a reader that does
not remove the first link keeps it. This case is ambiguous because `a` points either to `second`, or
to `first`, with an error for the second link or without one.

Decision point: whether a later member of the same name replaces an earlier one.
Seen in: none of the scanned tarballs.
See also: S07, the same file twice with different contents.
"""

VERDICT = "reject"
ID = "S24"
FEATURES = ["tree.duplicate.symlink-symlink"]


def build(a):
    a.file(b"first", b"first\n")
    a.file(b"second", b"second\n")
    a.symlink(b"a", b"first")
    a.symlink(b"a", b"second", note="a again, with another target")
    a.end()

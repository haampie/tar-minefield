"""A regular file followed by a symlink of the same name.

The archive has a file `t`, a file `a`, and a symlink `a` to `t`.

POSIX allows [overwriting existing files][overwritten], but `symlink()` [fails when the path already
exists][symlink-exists], so extracting the symlink requires unlinking `a` first. A reader that
removes the existing file extracts `a` as a symlink to `t`, whereas one that does not unlink it
leaves the regular file `a` in place (either reporting an error or skipping the symlink).

Decision point: whether a symlink replaces an earlier regular file of the same name.
Seen in: none of the scanned tarballs.
See also: S10, a symlink followed by a file of the same name.
"""

VERDICT = "reject"
ID = "S23"
FEATURES = ["tree.duplicate.file-symlink"]


def build(a):
    a.file(b"t", b"t\n")
    a.file(b"a", b"a file first\n")
    a.symlink(b"a", b"t", note="a symlink, after a file")
    a.end()

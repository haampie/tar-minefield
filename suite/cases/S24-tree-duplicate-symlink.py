"""Two symlinks with the same name and different targets: first wins, or last wins?

The archive has the files `first` and `second`, a symlink `a` to `first`, and a second symlink `a`
to `second`.

POSIX allows [overwriting existing files][overwrite] when an archive repeats a member name, but
`symlink()` [fails if the destination path exists][symlink-exists]. A reader that unlinks the
existing symlink before creating the new one leaves `a` pointing to `second`, whereas one that does
not unlink it leaves `a` pointing to `first` (either reporting an error or skipping the second
symlink).

Decision point: whether a duplicate symlink replaces the earlier one.
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
    a.symlink(b"a", b"second", note="second symlink a")
    a.end()

"""A member written through a symlink that points inside the destination.

The archive has the directories `d` and `x`, a symlink `x/l` to `../d`, and a file `x/l/f`.

Under [POSIX][resolution], files are created by pathname resolution, which
[follows][symlink-followed] `x/l` and writes `d/f` inside the destination directory. A reader that
follows the symlink extracts `d/f`, whereas one that refuses to traverse symlinks either fails or
skips `f`. A reader that defers creating symlinks until after regular files first creates `x/l` as a
real directory for `x/l/f` and then fails when creating the symlink `x/l`. It is rejected, as is
writing through any symlink: a reader that writes through links stays inside the destination only if
it resolves each link at every write.

Decision point: whether a member may be written through a symlink.
Seen in: none of the scanned tarballs.
See also: S10, a file at the path of a symlink, and S11, a member written through a symlink that
points out of the destination.
"""

VERDICT = "reject"
ID = "S19"
FEATURES = ["tree.through-symlink"]


def build(a):
    a.directory(b"d")
    a.directory(b"x")
    a.symlink(b"x/l", b"../d")
    a.file(b"x/l/f", b"f\n", note="written through x/l, to d/f")
    a.end()

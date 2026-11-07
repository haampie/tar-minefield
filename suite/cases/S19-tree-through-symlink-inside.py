"""A member written through a symlink that points inside the destination.

The archive has the directories `d` and `x`, a symlink `x/l` to `../d`, then a file `x/l/f`.

In [POSIX][resolution], files are created by pathname resolution, which [follows][symlink-followed]
the link, so the file is written to `d/f`, inside the destination. This case is ambiguous in
practice because a reader that writes through the link extracts `d/f`, and one that does not either
fails or skips `f`. A reader that creates symlinks after the other members writes `f` to a directory
`x/l`, and then fails to create the link. It is rejected, as is writing through any symlink: a
reader that writes through links stays inside the destination only if it resolves each link at every
write.

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

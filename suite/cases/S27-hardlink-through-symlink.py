"""A hardlink whose target is reached through a symlink.

The archive has a directory `d/` with a file `d/f`, a symlink `s` to `d`, then a hardlink `h` to
`s/f`.

In [POSIX][hardlink], the target of a hardlink is a file archived before it, and `s/f` is not the
name of a member. As a path, `s/f` resolves through the symlink to `d/f`, which is a member. This
case is ambiguous because `h` is either a link to `d/f`, to a reader that resolves the target as a
path on the filesystem, or an [error][link-error], to one that takes the target for the name of a
member. Neither reading skips the link without an error, as some readers do.

Decision point: whether the target of a hardlink is a path or the name of a member.
Seen in: none of the scanned tarballs.
See also: S16, a hardlink to `./a`, and S11, a member written through a symlink.
"""

VERDICT = "reject"
ID = "S27"
FEATURES = ["hardlink.missing-target"]


def build(a):
    a.directory(b"d/")
    a.file(b"d/f", b"f\n")
    a.symlink(b"s", b"d")
    a.hardlink(b"h", b"s/f", note="a target through the symlink s")
    a.end()

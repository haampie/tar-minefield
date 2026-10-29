"""A symlink whose name ends in a slash.

The archive has a directory `target/`, then a symlink `link/` to `target`. With the slash, the name
refers to what the link points to.

In [POSIX][file-type], a member is extracted as a file of its own type, here a symlink, but
`symlink()` [fails on a name][symlink-slash] that ends in a slash, so this is an
[error][cannot-create], or, as for an [invalid filename][invalid-name], it is up to the
implementation whether to create the symlink `link`. This case is ambiguous in practice because the
member is either a symlink `link`, by its typeflag, or a directory `link`, by its trailing slash.

Decision point: what a trailing slash on a link means.
Seen in: none of the scanned tarballs.
See also: K01, a regular file whose name ends in a slash.
"""

VERDICT = "reject"
ID = "K03"
FEATURES = ['name.trailing-slash-on-symlink']


def build(a):
    a.directory(b"target/")
    a.symlink(b"link/", b"target")
    a.end()

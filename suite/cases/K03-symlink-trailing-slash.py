"""A symlink whose name ends in a slash.

The archive has a directory `target/`, followed by a symlink `link/` to `target`. With the trailing
slash, the name refers to what the link points to.

Under [POSIX][file-type], a member is extracted with its archived file type (here a symlink), yet
`symlink()` [fails on a path][symlink-slash] ending in a slash, resulting in an
[error][cannot-create]. A reader that strips the trailing slash extracts a symlink `link`, whereas
one that classifies the member by its trailing slash extracts a directory `link`.

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

"""A symlink whose name ends in a slash.

The member `link/` is a symlink to `target`. With the slash, the name refers to what the link points
to. This case is ambiguous because the member is either a symlink `link`, by its typeflag, or a
directory `link`, by its trailing slash, as in K01.

Decision point: what a trailing slash on a link means.
Seen in: no source tarball.
"""

VERDICT = "reject"
ID = "K03"
FEATURES = ['name.trailing-slash-on-symlink']


def build(a):
    a.directory(b"target/")
    a.symlink(b"link/", b"target")
    a.end()

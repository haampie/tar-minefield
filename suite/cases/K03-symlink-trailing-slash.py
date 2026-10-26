"""A symlink whose name ends in a slash.

The first member is a directory `target/`, the second a symlink `link/` to `target`. With the slash,
the name refers to what the link points to. This case is ambiguous because the member is either a
symlink `link`, by its typeflag, or a directory `link`, by its trailing slash, as in K01. A reader
that takes it for neither makes an empty file `link`.

Decision point: what a trailing slash on a link means.
Seen in: none of the scanned tarballs.
"""

VERDICT = "reject"
ID = "K03"
FEATURES = ['name.trailing-slash-on-symlink']


def build(a):
    a.directory(b"target/")
    a.symlink(b"link/", b"target")
    a.end()

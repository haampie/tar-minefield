"""A hardlink whose name ends in a slash: a link, or a directory?

The archive has a file `a`, followed by a hardlink `b/` to `a`.

A [hardlink][hardlink] links to a previously archived file. Because a pathname ending in a slash
[resolves only to a directory][trailing-slash], a link to the regular file `a` cannot be a
directory, resulting in an [error][cannot-create]. A reader that strips the trailing slash extracts
a hardlink `b`. A reader that classifies the member by its trailing slash extracts a directory `b`,
while one that makes a regular file of a link it cannot create extracts an empty file `b`.

Decision point: whether the typeflag or the trailing slash decides the kind of a link.
Seen in: none of the scanned tarballs.
See also: K01, a regular file whose name ends in a slash, and K03, a symlink whose name ends in a
slash.
"""

VERDICT = "reject"
ID = "K05"
FEATURES = ["name.trailing-slash-on-hardlink"]


def build(a):
    a.file(b"a", b"a\n")
    a.hardlink(b"b/", b"a", note="a hardlink whose name ends in a slash")
    a.end()

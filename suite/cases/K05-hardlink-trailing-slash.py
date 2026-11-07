"""A hardlink whose name ends in a slash: a link, or a directory?

The archive has a file `a`, then a hardlink `b/` to `a`.

A [hardlink][hardlink] is a link to a file archived before it. A name that ends in a slash [resolves
only to a directory][trailing-slash], and a link to the regular file `a` cannot be one, so this is
an [error][cannot-create]. This case is ambiguous in practice because a reader can take the member
in one of three ways. A reader that drops the slash extracts a hardlink `b`. One that goes by the
slash extracts a directory `b`. One that makes a regular file of a link it cannot create extracts an
empty file `b`.

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

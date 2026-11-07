"""A hardlink whose name ends in a slash: a link, or a directory?

The archive has a file `a`, then a hardlink `b/` to `a`.

A [hardlink][hardlink] is a link to a file archived before it, but a name that ends in a slash
[resolves only to a directory][trailing-slash], which a link to a regular file cannot be, so this is
an [error][cannot-create]. This case is ambiguous in practice because the member is a hardlink `b`,
with the slash dropped, a directory `b`, by the slash, or an empty file `b`, to a reader that
makes a regular file of a link it cannot create.

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

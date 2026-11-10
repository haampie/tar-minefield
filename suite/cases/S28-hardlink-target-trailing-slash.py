"""A hardlink to `a/`, where `a` is a file.

The archive has a file `a`, then a hardlink `h` whose target is `a/`.

A pathname that ends in a slash [resolves only to a directory][trailing-slash], and `a` is a file,
so as a path the target does not resolve, and a link that cannot be made is an [error][link-error].
This case is ambiguous because `h` is either a link to `a`, to a reader that normalizes the target
as it normalizes names, or an error, to one that resolves the target as a path. Neither reading
skips the link without an error, as some readers do.

Decision point: whether the target of a hardlink is normalized.
Seen in: not measured, as earlier versions of the scanner normalized the targets of hardlinks: 2 of
the scanned tarballs may have such a target.
See also: S16, a hardlink to `./a`, which is tolerated, and K05, a hardlink whose name ends in a
slash.
"""

VERDICT = "reject"
ID = "S28"
FEATURES = ["hardlink.target-trailing-slash"]


def build(a):
    a.file(b"a", b"a\n")
    a.hardlink(b"h", b"a/", note="the target spelled a/")
    a.end()

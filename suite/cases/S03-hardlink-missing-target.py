"""A hardlink to a member that is not in the archive.

The archive has one member, `h`, a hardlink to `missing`, which is not in the archive.

In [POSIX][hardlink], the target of a hardlink is a file previously archived, which `missing` is
not, and a link that cannot be made is an [error][link-error]. This case is ambiguous because the
link is either an error, or, as data may also be [restored from the original file][restore], made to
a file of that name that already exists where the archive is extracted.

Decision point: what a hardlink to nothing does.
Seen in: none of the scanned tarballs.
"""

VERDICT = "reject"
ID = "S03"
FEATURES = ['hardlink.missing-target']


def build(a):
    a.hardlink(b"h", b"missing")
    a.end()

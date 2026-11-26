"""A hardlink to a member that is not in the archive.

The archive has one member, `h`, a hardlink to `missing`, which is not in the archive.

In [POSIX][hardlink], a hardlink refers to a previously archived file, and an uncreatable link is an
[error][link-error]. However, because POSIX also allows [restoring data from the original
file][restore], a reader that resolves hardlink targets directly on the destination filesystem can
link `h` to a pre-existing file named `missing` (or create an empty fallback file / skip the link).

Decision point: what a hardlink to nothing does.
Seen in: none of the scanned tarballs.
"""

VERDICT = "reject"
ID = "S03"
FEATURES = ['hardlink.missing-target']


def build(a):
    a.hardlink(b"h", b"missing")
    a.end()

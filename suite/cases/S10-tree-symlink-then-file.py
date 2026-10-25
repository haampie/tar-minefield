"""A symlink, then a file of the same name: replace the link, or write through it?

The first member is a symlink `a` to `target`, the second a file `a`. This case is ambiguous because
the file either replaces the link, or is written through it, to `target`.

Decision point: whether writing a member follows a symlink in its place.
Seen in: no source tarball.
"""

VERDICT = "reject"
ID = "S10"
FEATURES = ['tree.duplicate.symlink-file']


def build(a):
    a.symlink(b"a", b"target")
    a.file(b"a", b"written to a, or to target?\n")
    a.end()

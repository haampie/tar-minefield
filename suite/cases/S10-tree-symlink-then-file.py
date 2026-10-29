"""A symlink, then a file of the same name: replace the link, or write through it?

The archive has a symlink `a` to `target`, then a file `a`.

In [POSIX][resolution], files are created by pathname resolution, which follows a symlink, but a
member is also extracted as a file of its [own type][file-type]. This case is ambiguous because the
file either replaces the link, or is written through it, to `target`.

Decision point: whether writing a member follows a symlink in its place.
Seen in: none of the scanned tarballs.
"""

VERDICT = "reject"
ID = "S10"
FEATURES = ['tree.duplicate.symlink-file']


def build(a):
    a.symlink(b"a", b"target")
    a.file(b"a", b"written to a, or to target?\n")
    a.end()

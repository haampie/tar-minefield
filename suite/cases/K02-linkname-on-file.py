"""A regular file with a link target.

The header has typeflag `0` and the linkname `target`. POSIX gives a linkname meaning only for
links, and every implementation that accepts the archive extracts a file. The case is rejected
because the linkname contradicts the typeflag, not because it is ambiguous.

Decision point: whether a linkname makes a member a link.
Seen in: bgen 1.1.7.
"""

VERDICT = "reject"
ID = "K02"
FEATURES = ['linkname.on-file']


def build(a):
    a.file(b"a", b"a file, or a link?\n", linkname=b"target")
    a.end()

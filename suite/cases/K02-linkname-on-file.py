"""A regular file with a link target.

The header has typeflag `0` and the linkname `target`. POSIX gives a linkname meaning only for
links. This case is ambiguous because the member is either a file, by its typeflag, or a link to
`target`, by its linkname.

Decision point: whether a linkname makes a member a link.
Seen in: bgen 1.1.7.
"""

VERDICT = "reject"
ID = "K02"
FEATURES = ['linkname.on-file']
POSIX = "linkname"


def build(a):
    a.file(b"a", b"a file, or a link?\n", linkname=b"target")
    a.end()

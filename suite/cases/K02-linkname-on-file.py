"""A regular file with a link target.

The header has typeflag `0` and the linkname `target`. [POSIX][linkname] gives a linkname meaning
only for links, and extracts a member as a file of its [own type][file-type], so the member is a
file. This case is ambiguous only to a reader that goes by the linkname, and makes a link to
`target`.

Decision point: whether a linkname makes a member a link.
Seen in: bgen 1.1.7.
"""

VERDICT = "reject"
ID = "K02"
FEATURES = ['linkname.on-file']


def build(a):
    a.file(b"a", b"a file, or a link?\n", linkname=b"target")
    a.end()

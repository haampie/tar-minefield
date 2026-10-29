"""A symlink with an empty target.

The archive has one symlink, `link`, whose linkname field is empty.

A symlink to the empty string cannot be created on most systems. [POSIX][symlink] allows it: the
contents of a symlink are stored in its linkname field, and `symlink()` [takes them as a
string][symlink-string], not as a pathname; where the system refuses to create it, pax writes a
["diagnostic message"][cannot-create]. This case is ambiguous because the tree depends on the
system: a symlink `link` with an empty target, or none.

Decision point: whether a link with an empty target is a link.
Seen in: none of the scanned tarballs.
"""

VERDICT = "reject"
ID = "N25"
FEATURES = ["symlink.empty-target"]


def build(a):
    a.symlink(b"link", b"", note="a symlink whose target is empty")
    a.end()

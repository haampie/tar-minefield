"""A symlink with an empty target.

The archive has one symlink, `link`, whose linkname field is empty, and no pax `linkpath`.

A symlink to the empty string cannot be created on most systems. [POSIX][symlink] allows it: the
contents of a symlink are stored in its linkname field, and `symlink()` [takes them as a
string][symlink-string], not as a pathname; where the system refuses to create it, pax
[reports][cannot-create] that it cannot create the link. This case is ambiguous in practice because
readers fail, make an empty file, skip the member, or make a link to `.`.

Decision point: whether a link with an empty target is a link.
Seen in: none of the scanned tarballs.
"""

VERDICT = "reject"
ID = "N25"
FEATURES = ["symlink.empty-target"]


def build(a):
    a.symlink(b"link", b"", note="a symlink whose target is empty")
    a.end()

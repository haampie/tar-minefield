"""A symlink with an empty target.

The member `link` is a symlink whose linkname field is empty, and there is no pax `linkpath`. A
symlink to the empty string cannot be created on most systems. This case is ambiguous because POSIX
says only that the contents of a symlink are stored in its linkname field, which leaves room for
interpretation of what an empty name means.

Decision point: whether a link with an empty target is a link.
Seen in: none of the scanned tarballs.
"""

VERDICT = "reject"
ID = "N25"
FEATURES = ["symlink.empty-target"]
POSIX = "symlink"


def build(a):
    a.symlink(b"link", b"", note="a symlink whose target is empty")
    a.end()

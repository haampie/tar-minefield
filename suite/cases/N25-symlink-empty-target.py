"""A symlink with an empty target.

The member `link` is a symlink whose linkname field is empty, and there is no pax `linkpath`. A
symlink to the empty string cannot be created on most systems, and POSIX says only that the contents
of the link are stored in the linkname field. This case is ambiguous because the member is a symlink
to the empty string, which some systems allow, or no member at all, or, read by what can be created,
an empty regular file `link`, which changes its kind.

Decision point: whether a link with an empty target is a link.
Seen in: none of the scanned tarballs.
"""

VERDICT = "reject"
ID = "N25"
FEATURES = ["symlink.empty-target"]


def build(a):
    a.symlink(b"link", b"", note="a symlink whose target is empty")
    a.end()

"""A symlink with an empty target.

The member `link` is a symlink whose linkname field is empty, and there is no pax `linkpath`. A
symlink to the empty string cannot be created on most systems. POSIX allows it: the contents of a
symlink are stored in its linkname field, and
[`symlink()`](https://pubs.opengroup.org/onlinepubs/9799919799/functions/symlink.html#:~:text=shall%20be%20treated%20only%20as%20a%20string%20and%20shall%20not%20be%20validated%20as%20a%20pathname)
takes them as a string, not as a pathname; where the system refuses to create it, pax reports that
it cannot create the link. This case is ambiguous in practice because readers fail, make an empty
file, skip the member, or make a link to `.`.

Decision point: whether a link with an empty target is a link.
Seen in: none of the scanned tarballs.
"""

VERDICT = "reject"
ID = "N25"
FEATURES = ["symlink.empty-target"]
POSIX = {"POSIX": "symlink", "reports": "cannot-create"}


def build(a):
    a.symlink(b"link", b"", note="a symlink whose target is empty")
    a.end()

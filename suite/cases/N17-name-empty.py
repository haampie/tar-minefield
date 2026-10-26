"""A member with an empty name.

The name field is all NULs. In POSIX, it is implementation-defined whether a member with an invalid
name is stored, and under what name. This case is ambiguous because an empty name marks the end of
the archive, leaves the member out, or refers to the destination directory itself.

Decision point: what an empty name refers to.
Seen in: none of the scanned tarballs.
"""

VERDICT = "reject"
ID = "N17"
FEATURES = ['name.empty']
POSIX = "invalid-name"


def build(a):
    a.file(b"", b"no name\n")
    a.end()

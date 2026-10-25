"""A member with an empty name.

The name field is all NULs. In POSIX, it is implementation-defined whether a member with an invalid
name is stored, and under what name. This case is ambiguous because an empty name marks the end of
the archive, leaves the member out, or refers to the destination directory itself.

Decision point: what an empty name refers to.
Seen in: no source tarball.
"""

VERDICT = "reject"
ID = "N17"
FEATURES = ['name.empty']


def build(a):
    a.file(b"", b"no name\n")
    a.end()

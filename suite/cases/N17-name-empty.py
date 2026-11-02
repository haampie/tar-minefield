"""A member with an empty name.

The archive has one file whose name field is all NULs.

The name is an empty pathname, which [does not resolve][null-pathname], so it would create an
invalid filename. In [POSIX][invalid-name], it is then implementation-defined whether the member is
stored, and under what name, and the member may be [ignored][ignore-invalid], with an error. This
case is ambiguous because it is implementation-defined whether the member is skipped with an error,
or stored under a name the implementation chooses.

Decision point: what an empty name refers to.
Seen in: none of the scanned tarballs.
"""

VERDICT = "reject"
ID = "N17"
FEATURES = ['name.empty']


def build(a):
    a.file(b"", b"no name\n")
    a.end()

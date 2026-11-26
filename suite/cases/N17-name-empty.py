"""A member with an empty name.

The archive has one file whose name field is all NULs.

An empty pathname [does not resolve][null-pathname]. Under [POSIX][invalid-name], it is
implementation-defined whether a member with an invalid filename is extracted and under what name,
or [skipped with an error][ignore-invalid].

Decision point: what an empty name refers to.
Seen in: none of the scanned tarballs.
"""

VERDICT = "reject"
ID = "N17"
FEATURES = ['name.empty']


def build(a):
    a.file(b"", b"no name\n")
    a.end()

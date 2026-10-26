"""A member with an empty name.

The name field is all NULs. In POSIX, it is implementation-defined whether a member with an invalid
name is stored, and under what name. This case is ambiguous because implementations read an empty
name in different ways: Rust's tar, astral-tokio-tar, containerd and live-bootstrap skip the member,
7-Zip names the file after the archive, and the others reject it.

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

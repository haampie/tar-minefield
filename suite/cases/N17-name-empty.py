"""A member with an empty name.

The name field is all NULs. In POSIX, it is implementation-defined whether a member with an invalid
name is stored, and under what name. This case is ambiguous because implementations read an empty
name in different ways: a reader skips the member, names the file after the archive, takes the name
for the destination directory itself, and fails to write a file there, or takes the header for the
end of the archive.

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

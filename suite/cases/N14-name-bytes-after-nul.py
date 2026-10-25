r"""Bytes after the NUL that ends a name.

The name field contains `a`, a NUL, and `b`. In POSIX, a name ends at its first NUL, so the name is
`a`. This case is still ambiguous because the name can also be read as the whole field, `a\0b`,
which is `ab` once the NUL is dropped.

Decision point: where a name ends.
Seen in: no source tarball.
"""

VERDICT = "reject"
ID = "N14"
FEATURES = ['name.bytes-after-nul']


def build(a):
    a.file(b"a\0b", b"a, or ab?\n")
    a.end()

r"""Bytes after the NUL that ends a name.

The name field holds `a`, a NUL, and `b`. In POSIX, a name ends at its first NUL, so the name is
`a`, and every implementation that accepts the archive extracts that. The case is rejected because
the bytes after the NUL hold a name that only a reader of the whole field sees, not because the
archive is ambiguous.

Decision point: where a name ends.
Seen in: no source tarball.
"""

VERDICT = "reject"
ID = "N14"
FEATURES = ['name.bytes-after-nul']


def build(a):
    a.file(b"a\0b", b"a, or ab?\n")
    a.end()

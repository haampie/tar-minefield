r"""Bytes after the NUL that ends a name.

The name field contains `a`, followed by a NUL, followed by `b`. In POSIX, a name ends at its first
NUL, so the name is `a`. Copied as a whole, the field is `a` as a C string, which ends at the first
NUL, but `a\0b` in languages whose strings can contain a NUL, and creating the file then fails.

Decision point: where a name ends.
Seen in: none of the scanned tarballs.
"""

VERDICT = "reject"
ID = "N14"
FEATURES = ['name.bytes-after-nul']
POSIX = "name-nul"


def build(a):
    a.file(b"a\0b", b"a, or ab?\n")
    a.end()

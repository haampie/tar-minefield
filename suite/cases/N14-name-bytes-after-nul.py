r"""Bytes after the NUL that ends a name.

The archive has one file whose name field contains `a`, followed by a NUL, followed by `b`.

In [POSIX][name-nul], a name ends at its first NUL, so the name is `a`. Copied as a whole, the field
is `a` as a C string, which ends at the first NUL, but `a\0b` in languages whose strings can contain
a NUL, and creating the file then fails.

The bytes after the NUL have no meaning and no writer puts them there (none of the scanned tarballs
has them), so a strict parser rejects them rather than guess what they are for.

Decision point: where a name ends.
Seen in: none of the scanned tarballs.
"""

VERDICT = "reject"
ID = "N14"
FEATURES = ['name.bytes-after-nul']


def build(a):
    a.file(b"a\0b", b"a, or ab?\n")
    a.end()

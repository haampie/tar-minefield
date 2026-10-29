r"""The POSIX magic with a version that is neither `00` nor NULs.

The archive has one file, `a`, whose magic `ustar\0` is followed by the version `01`.

[POSIX][version] requires `00`. The default policy accepts only that version, and NULs as some Java
archivers write. This case is ambiguous because a reader takes the header in one of three ways: as
ustar, ignoring the version; as not in a format that POSIX defines, and stops; or as a v7 header,
without the fields that ustar added, which here are empty, so that it gives the same tree.

Decision point: which format the header is in.
Seen in: none of the scanned tarballs.
"""

VERDICT = "reject"
ID = "F11"
FEATURES = ['magic.posix-with-odd-version']


def build(a):
    a.file(b"a", b"a\n", version=b"01")
    a.end()

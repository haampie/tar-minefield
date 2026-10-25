r"""The POSIX magic with a version that is neither `00` nor NULs.

The magic `ustar\0` is followed by the version `01`, where POSIX requires `00`. The default policy
accepts only that version, and NULs as some Java archivers write. This breaks POSIX, which is why
the case is rejected; it is not ambiguous.

Decision point: which format the header is in.
Seen in: no source tarball.
"""

VERDICT = "reject"
ID = "F11"
FEATURES = ['magic.posix-with-odd-version']


def build(a):
    a.file(b"a", b"a\n", version=b"01")
    a.end()

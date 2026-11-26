r"""The POSIX magic with a version that is neither `"00"` nor NULs.

The archive has one file, `a`, with magic `"ustar\0"` and version `"01"`.

In [POSIX][version], the version field is `"00"`. The default policy also tolerates two NULs, as
written by some Java archivers, but rejects any other version. A reader may ignore the version and
parse the header as ustar, reject the header as an unknown format, or fall back to treating it as a
v7 header without the ustar fields.

Decision point: which format the header is in.
Seen in: none of the scanned tarballs.
See also: F05, the POSIX magic with NULs for its version, which is tolerated.
"""

VERDICT = "reject"
ID = "F11"
FEATURES = ['magic.posix-with-odd-version']


def build(a):
    a.file(b"a", b"a\n", version=b"01")
    a.end()

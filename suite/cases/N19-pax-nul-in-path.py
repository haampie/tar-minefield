r"""A NUL inside a pax `path`.

The archive has one file with `path=a\0b` in its pax header and `header-name` in its ustar name
field.

In [POSIX][value-data], every byte in a pax value is data, so the path contains an [embedded
NUL][embedded-nul] and pax [bypasses][bypass] the file by default. Readers that do not reject the
archive either truncate the path at the NUL to `a`, replace the NUL to form a name like `a_b`, or
discard the pax record and fall back to `header-name`.

Decision point: where a pax path ends.
Seen in: none of the scanned tarballs.
"""

VERDICT = "reject"
ID = "N19"
FEATURES = ['pax.nul-in-value.path']


def build(a):
    a.pax([(b"path", b"a\0b")])
    a.file(b"header-name", b"a, or a\\0b?\n")
    a.end()

r"""A NUL inside a pax `path`.

The pax path is `a\0b`. In [POSIX][value-data], a NUL in a pax value is data, so the path is
invalid, and pax by default [bypasses][bypass] a file whose name has an [embedded
NUL][embedded-nul]. This case is ambiguous in practice because the path is `a`, cut at the NUL,
`a_b` or the like, with the NUL replaced, or discarded for the header's name, `header-name`.

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

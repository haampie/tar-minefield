r"""A NUL inside a pax `path`.

The pax path is `a\0b`. In POSIX, a NUL in a pax value is data, so the path is invalid, and it is
implementation-defined whether the member is stored, and under what name. This case is ambiguous
because the path is `a`, cut at the NUL, `a_b` or the like, with the NUL replaced, or discarded for
the header's name, `header-name`.

Decision point: where a pax path ends.
Seen in: no source tarball.
"""

VERDICT = "reject"
ID = "N19"
FEATURES = ['pax.nul-in-value.path']


def build(a):
    a.pax([(b"path", b"a\0b")])
    a.file(b"header-name", b"a, or a\\0b?\n")
    a.end()

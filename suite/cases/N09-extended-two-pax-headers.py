"""Two pax extended headers for one member, with different paths.

The archive has two `x` headers, with `path=first` and `path=second`, then the member, whose header
has the name `header-name`.

[POSIX][last-wins] settles conflicting records within one extended header, where the last one wins,
but two extended headers for one file break the [sequence][sequence] that POSIX describes, and it
does not say how to read them. This case is ambiguous because the name is `first`, `second`, or the
header's own.

Decision point: which of two extended headers of one kind applies.
Seen in: none of the scanned tarballs. libmygpo-qt 1.2.0 repeats xattr keys within one header.
See also: N20, one pax key twice in one extended header.
"""

VERDICT = "reject"
ID = "N09"
FEATURES = ['extended.two-pax-headers']


def build(a):
    a.pax([(b"path", b"first")])
    a.pax([(b"path", b"second")])
    a.file(b"header-name", b"which name?\n")
    a.end()

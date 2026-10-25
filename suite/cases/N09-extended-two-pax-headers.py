"""Two pax extended headers for one member, with different paths.

Two `x` headers come before one member, with the paths `first` and `second`. POSIX settles
conflicting records within one extended header, where the last one wins, but not two extended
headers for one file. This case is ambiguous because the name is `first`, `second`, or the header's
own.

Decision point: which of two extended headers of one kind applies.
Seen in: no source tarball. libmygpo-qt 1.2.0 repeats xattr keys within one header, which is
N20, pax-repeated-key.
"""

VERDICT = "reject"
ID = "N09"
FEATURES = ['extended.two-pax-headers']
POSIX = "last-wins"


def build(a):
    a.pax([(b"path", b"first")])
    a.pax([(b"path", b"second")])
    a.file(b"header-name", b"which name?\n")
    a.end()

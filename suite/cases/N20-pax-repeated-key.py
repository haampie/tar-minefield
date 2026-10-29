"""One pax key twice in one extended header.

The extended header has the records `path=first` and `path=second`. In [POSIX][last-wins], the last
of conflicting records in one header takes precedence, so the name is `second`. This case is
ambiguous in practice because the name is also read as `first`, or as the header's own, with the
records discarded.

Decision point: which of two values of one key applies.
Seen in: libmygpo-qt 1.2.0, with xattr keys.
"""

VERDICT = "reject"
ID = "N20"
FEATURES = ['pax.repeated-key']


def build(a):
    a.pax([(b"path", b"first"), (b"path", b"second")])
    a.file(b"header-name", b"which name?\n")
    a.end()

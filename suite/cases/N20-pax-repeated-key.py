"""One pax key twice in one extended header.

The archive has one file with both `path=first` and `path=second` in its pax header, and
`header-name` in its ustar name field.

When records in the same pax header conflict, [POSIX][last-wins] gives precedence to the last one,
making the filename `second`. However, some readers keep the first record (`first`) or discard the
conflicting records and fall back to `header-name`.

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

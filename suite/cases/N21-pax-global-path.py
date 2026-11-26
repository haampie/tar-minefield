"""A global pax header with a `path`.

The archive starts with a global header containing `path=global-name`, followed by the files `a` and
`b`.

In [POSIX][global], a global header applies to every subsequent member that does not override it,
giving both files the name `global-name`. A reader that ignores `path` in a global header instead
extracts `a` and `b` under their own ustar names.

Decision point: whether a global `path` applies.
Seen in: none of the scanned tarballs.
"""

VERDICT = "reject"
ID = "N21"
FEATURES = ['pax-global.path']


def build(a):
    a.pax([(b"path", b"global-name")], typeflag=b"g", name=b"pax_global_header")
    a.file(b"a", b"a\n")
    a.file(b"b", b"b\n")
    a.end()

"""A global pax header with a `path`.

In [POSIX][global], a global header applies to every later member, so with a `path` all of them have
one name, `global-name`. This case is ambiguous in practice because, with the global `path` ignored,
the members keep their own names, `a` and `b`.

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

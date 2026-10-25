"""A global pax header between an extended header and its member.

An `x` header, then a `g` header, then the member. In POSIX, an extended header applies to the
following file, but whether a global header counts as one is left open. This case is ambiguous
because the extended header applies either to the global header, and the member keeps its name,
`header-name`, or to the member, as `from-pax`.

Decision point: which header an extended header applies to.
Seen in: no source tarball.
"""

VERDICT = "reject"
ID = "F19"
FEATURES = ['pax-global.between-extended-and-member']
POSIX = "extended"


def build(a):
    a.pax([(b"path", b"from-pax")])
    a.pax([(b"comment", b"between")], typeflag=b"g", name=b"pax_global_header")
    a.file(b"header-name", b"which name?\n")
    a.end()

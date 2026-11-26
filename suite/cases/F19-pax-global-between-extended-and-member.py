"""A global pax header between an extended header and its member.

The archive has an `x` extended header with `path=from-pax`, followed by a `g` global header with
only a `comment`, and then a file whose ustar header gives the name `header-name`.

In [POSIX][extended], an extended header applies to the file that follows it, while a global header
is not a file but [metadata for subsequent files][global-files]. However, POSIX
[describes][sequence] each member as preceded by at most one extended or global header, leaving an
`x` header followed by a `g` header unspecified. A reader that attaches `x` to the immediately
following `g` header discards `path=from-pax` and extracts `header-name`, whereas one that carries
`x` across the global header to the file extracts `from-pax`.

Decision point: which header an extended header applies to.
Seen in: none of the scanned tarballs.
"""

VERDICT = "reject"
ID = "F19"
FEATURES = ['pax-global.between-extended-and-member']


def build(a):
    a.pax([(b"path", b"from-pax")])
    a.pax([(b"comment", b"between")], typeflag=b"g", name=b"pax_global_header")
    a.file(b"header-name", b"which name?\n")
    a.end()

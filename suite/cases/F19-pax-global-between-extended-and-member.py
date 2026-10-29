"""A global pax header between an extended header and its member.

An `x` header, then a `g` header, then the member. In POSIX, an extended header applies to the
following file, and a global header is not a file but records for the files after it. But POSIX
describes each file as at most one extended or global header, then its own header, so this sequence
is not one it describes, and it does not say how to read it. This case is ambiguous because the
extended header applies either to the global header, and the member keeps its name, `header-name`,
or to the member, as `from-pax`.

Decision point: which header an extended header applies to.
Seen in: none of the scanned tarballs.
"""

VERDICT = "reject"
ID = "F19"
FEATURES = ['pax-global.between-extended-and-member']
POSIX = {"POSIX": "extended", "records for the files": "global-files", "describes": "sequence"}


def build(a):
    a.pax([(b"path", b"from-pax")])
    a.pax([(b"comment", b"between")], typeflag=b"g", name=b"pax_global_header")
    a.file(b"header-name", b"which name?\n")
    a.end()

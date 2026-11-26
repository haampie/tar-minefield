"""A pax `GNU.sparse.name` on a file that is not sparse, after a `path`.

The archive has a file whose pax header contains `path=path-name` followed by
`GNU.sparse.name=sparse-name` (with no other GNU sparse records), and whose ustar header gives the
name `header-name`.

In GNU's pax sparse format, `GNU.sparse.name` holds the real filename of a sparse member. Under
POSIX, vendor keywords are [optional extensions][keyword-extension]. A reader that applies
`GNU.sparse.name` unconditionally (either because it takes priority over `path` or because it comes
later in the header) extracts `sparse-name`. A reader that ignores `GNU.sparse.name` on a non-sparse
file extracts `path-name`, while one that discards both records extracts `header-name`.

Decision point: whether `GNU.sparse.name` applies to a file that is not sparse.
Seen in: none of the scanned tarballs.
See also: N36, a sparse file in GNU's pax format.
"""

VERDICT = "reject"
ID = "N41"
FEATURES = ["pax.gnu-sparse"]


def build(a):
    a.pax([(b"path", b"path-name"), (b"GNU.sparse.name", b"sparse-name")])
    a.file(b"header-name", b"which name?\n")
    a.end()

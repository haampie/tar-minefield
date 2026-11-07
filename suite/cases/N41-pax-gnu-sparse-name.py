"""A pax `GNU.sparse.name` on a file that is not sparse, after a `path`.

The archive has a file whose pax header has the records `path=path-name`, then
`GNU.sparse.name=sparse-name`, and whose header has the name `header-name`. The pax header does not
have other records of GNU's sparse format.

In GNU's pax format of sparse files, the name of a sparse file is in `GNU.sparse.name`. In POSIX,
keywords such as GNU's are allowed as [implementation extensions][keyword-extension], and are not
defined. This case is ambiguous because the name is either `sparse-name` or `path-name`. A reader
that applies `GNU.sparse.name` to any file extracts `sparse-name`, either because it gives that
record precedence over `path`, or because it is the later of the two. A reader that applies it only
to a sparse file extracts `path-name`, and one that ignores both records extracts `header-name`.

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

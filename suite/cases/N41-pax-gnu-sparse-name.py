"""A pax `GNU.sparse.name` on a file that is not sparse, after a `path`.

The archive has a file whose pax header has `path=path-name`, then `GNU.sparse.name=sparse-name`,
and whose header has the name `header-name`. The pax header has no other keys of GNU's sparse
format.

In GNU's pax format of sparse files, the name of a sparse file is in `GNU.sparse.name`. In POSIX,
keywords such as GNU's are [implementation extensions][keyword-extension], which are not defined.
This case is ambiguous because the name is `sparse-name`, to a reader that applies `GNU.sparse.name`
to any file, as the last of two records with a name, or `path-name`, to one that applies it only to
a sparse file.

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

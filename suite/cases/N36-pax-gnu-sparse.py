"""A sparse file in GNU's pax format 1.0: the data as stored, or the file it expands to?

The archive has one member whose pax header sets `GNU.sparse.major=1`, `GNU.sparse.minor=0`,
`GNU.sparse.name=a`, `GNU.sparse.realsize=1026` and `path=GNUSparseFile.0/a`. Its data consists of a
512-byte sparse map block (`1\n1024\n2\n` padded with NULs, describing a single 2-byte region at
offset 1024) followed by those 2 bytes, `ab`.

Under POSIX, vendor keywords such as `GNU.sparse.*` are [implementation
extensions][keyword-extension], which are not defined, so a reader that ignores them applies
[`path`][path] and extracts the unexpanded map and data to `GNUSparseFile.0/a`. A reader that
supports GNU sparse format 1.0 expands the file to 1024 zero bytes followed by `ab` under
`GNU.sparse.name` (`a`), while a reader that expands the sparse payload without applying
`GNU.sparse.name` writes the 1026-byte file to `GNUSparseFile.0/a`.

Decision point: whether a sparse member is expanded, and which of its names it gets.
Seen in: none of the scanned tarballs.
See also: F45, an old GNU sparse file.
"""

VERDICT = "reject"
ID = "N36"
FEATURES = ["pax.gnu-sparse"]


def build(a):
    sparse_map = b"1\n1024\n2\n"
    data = sparse_map + bytes(512 - len(sparse_map)) + b"ab"
    a.pax([(b"GNU.sparse.major", b"1"), (b"GNU.sparse.minor", b"0"), (b"GNU.sparse.name", b"a"),
           (b"GNU.sparse.realsize", b"1026"), (b"path", b"GNUSparseFile.0/a")],
          note="a sparse file in GNU's format 1.0")
    a.file(b"GNUSparseFile.0/a", data, note="the sparse map, then the one region of data")
    a.end()

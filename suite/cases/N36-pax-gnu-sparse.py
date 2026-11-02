"""A sparse file in GNU's pax format 1.0: the data as stored, or the file it expands to?

The archive has one member, whose pax header has `GNU.sparse.major=1`, `GNU.sparse.minor=0`,
`GNU.sparse.name=a`, `GNU.sparse.realsize=1026` and `path=GNUSparseFile.0/a`. Its data is a sparse
map of one region, 2 bytes at offset 1024, as the lines `1`, `1024` and `2` padded with NULs to a
block, followed by those 2 bytes, `ab`.

POSIX allows keys such as GNU's as extensions, but does not define them, so a reader that ignores
them applies the pax [`path`][path], and extracts `GNUSparseFile.0/a`, which holds the map and the
data. GNU's format
makes the member `a`, a file of 1026 bytes, zeros but for the last two. This case is ambiguous
because the member is the data as stored, under its pax `path`, or the file it expands to, under
`GNU.sparse.name`, or even the expanded file under the pax `path`.

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

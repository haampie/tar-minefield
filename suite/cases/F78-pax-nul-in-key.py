"""A NUL in a pax key, before a `path` record.

The archive has a file whose pax header has two records. The key of the first is `pa`, followed by a
NUL, followed by `th`, and its value is `x`. The second is `path=renamed`. The header of the file
has the name `header-name`.

pax records are delimited by their [length][record-length], so the first record has a key that
readers do not know, and the file is `renamed`. This case is ambiguous in practice because a reader
can take the header in one of three ways. A reader that reads the records by their length extracts
`renamed`. One that ends the data of a pax header at its first NUL, or discards a header that
contains one, loses the `path` record and extracts `header-name`. Other readers report an error.
Some tarballs have a NUL in the value of an xattr, and a reader must still apply the records after
it. A NUL in a key does not mean anything, so a strict parser rejects it.

Decision point: whether the records of a pax header end at a NUL in a key.
Seen in: not measured, as the scans do not record all pax keys of a tarball, only its 8 most common:
none of those has a NUL, and 9 of the scanned tarballs have more keys.
See also: F59, a NUL in the value of an xattr, which the default policy accepts, and N19, a NUL in a
pax `path`.
"""

VERDICT = "reject"
ID = "F78"
FEATURES = ["pax.nul-in-key"]


def build(a):
    a.pax([(b"pa\0th", b"x"), (b"path", b"renamed")], note="a key with a NUL, then a path")
    a.file(b"header-name", b"which name?\n")
    a.end()

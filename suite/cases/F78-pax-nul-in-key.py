"""A NUL in a pax key, before a `path` record.

The archive has a file whose pax header has two records. The key of the first is `pa`, followed by a
NUL, followed by `th`, and its value is `x`. The second is `path=renamed`. The header of the file
has the name `header-name`.

pax records are delimited by their [length][record-length], so the first record has a key that
readers do not know, and the second names the file `renamed`. This case is ambiguous in practice
because a reader that reads the records by their length extracts `renamed`, one that ends the data
of a pax header at its first NUL, or discards a header that contains one, loses the `path` record
and extracts `header-name`, and other readers report an error. A NUL in the value of an xattr occurs
in real archives, and a reader has to read past it. A NUL in a key does not have a use, so a strict
parser rejects it.

Decision point: whether a NUL in a pax key ends the records.
Seen in: not measured, as the scans record the 8 most common pax keys of a tarball: none of those
has a NUL, and at most 9 of the scanned tarballs have more keys.
See also: F59, a NUL in the value of an xattr, which is to accept, and N19, a NUL in a pax `path`.
"""

VERDICT = "reject"
ID = "F78"
FEATURES = ["pax.nul-in-key"]


def build(a):
    a.pax([(b"pa\0th", b"x"), (b"path", b"renamed")], note="a key with a NUL, then a path")
    a.file(b"header-name", b"which name?\n")
    a.end()

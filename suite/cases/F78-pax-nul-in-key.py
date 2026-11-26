"""A NUL byte inside a pax key, before a `path` record.

The archive has a file with two pax records. The first has the key `pa`, a NUL and `th`, and the
value `x`; the second is `path=renamed`. The file's ustar header gives the name `header-name`.

Because pax records are framed by their [byte length][record-length], a length-based parser treats
the first key as unknown and applies the following `path=renamed` record. A reader that stops
parsing the pax payload at the first NUL, or discards any pax header containing a NUL, loses
`path=renamed` and extracts `header-name`. Other readers report an error. Binary xattr values
contain NUL bytes in some published tarballs, and a reader must still apply the records that follow
them, but a NUL in a key has no meaning, so a strict parser rejects it.

Decision point: whether a NUL in a pax key truncates or invalidates the pax header.
Seen in: not measured, as the scanner records only the 8 most common pax keys per tarball; none of
those contains a NUL, and 9 scanned tarballs have additional keys.
See also: F59, a NUL in an xattr value, which the default policy accepts, and N19, a NUL in a pax
`path`.
"""

VERDICT = "reject"
ID = "F78"
FEATURES = ["pax.nul-in-key"]


def build(a):
    a.pax([(b"pa\0th", b"x"), (b"path", b"renamed")], note="a key with a NUL, then a path")
    a.file(b"header-name", b"which name?\n")
    a.end()

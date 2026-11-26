"""A v7 header first, then a member with a pax header: is the `x` header a header, or a file?

The archive has a file `a` with a v7 header (no magic), followed by a pax header with
`path=from-pax` and a file header named `from-header`, both carrying the POSIX magic.

POSIX requires [detecting the archive format][detected] on input, without specifying whether
detection happens once or per header. A reader that locks in the v7 format from the first header
does not recognize typeflag `x` and extracts the pax header as a regular file `PaxHeader` (just like
a [pre-pax ustar reader][pre-pax-reader]), followed by `from-header`. A reader that inspects each
header's magic applies the pax header and extracts `a` and `from-pax`.

Decision point: whether the format of an archive is decided once, by its first header, or for every
header.
Seen in: none of the scanned tarballs.
"""

VERDICT = "reject"
ID = "F39"
FEATURES = ["format.pax-after-v7"]


def build(a):
    a.file(b"a", b"a\n", magic=b"", version=b"", devmajor=b"", devminor=b"",
           note="no magic, and nothing after the linkname: a v7 header")
    a.pax([(b"path", b"from-pax")])
    a.file(b"from-header", b"which name?\n")
    a.end()

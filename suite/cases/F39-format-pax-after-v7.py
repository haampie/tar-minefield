"""A v7 header first, then a member with a pax header: is the `x` header a header, or a file?

The archive has a file `a` whose header is in the v7 format (without magic), then a pax header with
`path=from-pax`, then a file whose header has the name `from-header`. The pax header and the header
after it have the POSIX magic.

According to POSIX, a reader [should detect][detected] the format of an archive, but it is not
specified from which headers detection must happen. A reader that decides it once, from the first
header, parses it as a v7 archive, in which typeflag `x` is not defined: it should then extract
the pax header [as a regular file][pre-pax-reader], `PaxHeader`, and the member as `from-header`. A
reader that looks at the magic of every header applies the pax header, and extracts the member as
`from-pax`. This case is ambiguous because the tree has `a`, `PaxHeader` and `from-header`, or `a`
and `from-pax`, depending on how the format is detected.

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

r"""A pax extended header without magic: a header, or a file?

The archive has a header of typeflag `x`, without magic or version, whose data is the record
`path=renamed`, then a file whose header has the POSIX magic and the name `header-name`.

In POSIX, ustar and pax headers have the [magic][magic] `"ustar\0"`. This header has typeflag `x`
but no magic. This case is ambiguous because the file is `renamed` if the header is parsed as an
extended header, and `header-name` if it is not.

Decision point: whether a header without magic may be an extended header.
Seen in: none of the scanned tarballs.
See also: F39, a pax header after a v7 header.
"""

VERDICT = "reject"
ID = "F54"
FEATURES = ["format.pax-after-v7"]

RECORD = b"16 path=renamed\n"


def build(a):
    a.header(b"PaxHeader", b"x", len(RECORD), magic=b"", version=b"",
             note="no magic and no version")
    a.raw(RECORD, "data: pax records")
    a.file(b"header-name", b"which name?\n")
    a.end()

"""A pax extended header without magic: a header, or a file?

The archive has a pax header, typeflag `x`, without magic or version, whose data is the record
`path=renamed`, then a file whose header has the POSIX magic and the name `header-name`.

In POSIX, the format of an archive is [detected][detected] on input, but it is not specified from
which headers, and the [magic][magic] field specifies the format that the archive was written in: a
header without it is not one of ustar, or of pax, whose [header block is that of
ustar][pax-header-block]. To a [reader of ustar before pax][pre-pax-reader], an extended header is a
regular file. This case is ambiguous
because the member is `renamed`, to a reader that takes the header for an extended header by its
typeflag, or `header-name`, after a file `PaxHeader` that contains the record, or alone, to a reader
that skips it.

Decision point: whether a header without magic may be an extended header.
Seen in: none of the scanned tarballs.
See also: F39, a pax header after a v7 header.
"""

VERDICT = "reject"
ID = "F55"
FEATURES = ["format.pax-after-v7"]

RECORD = b"16 path=renamed\n"


def build(a):
    a.header(b"PaxHeader", b"x", len(RECORD), magic=b"", version=b"",
             note="no magic and no version")
    a.raw(RECORD, "data: pax records")
    a.file(b"header-name", b"which name?\n")
    a.end()

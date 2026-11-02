"""A Solaris extended header, typeflag `X`: a pax header, or a file?

The archive has a header of typeflag `X`, named `PaxHeader`, whose data is the pax record
`path=from-x`, then a file whose header has the name `from-header`.

Solaris tar writes extended headers with typeflag `X`, instead of the `x` of POSIX. In POSIX, the
typeflags `A` to `Z` are reserved for [custom implementations][custom-type], and a reader that does
not recognize one extracts the member [as a regular file][unknown-type]. This case is ambiguous
because the member is `from-x`, to a reader that takes `X` for `x`, or `from-header`, after a file
`PaxHeader` that contains the record, or alone, to a reader that skips a type it does not know.

Decision point: whether typeflag `X` is an extended header.
Seen in: none of the scanned tarballs.
See also: F16, an unknown typeflag with a size.
"""

VERDICT = "reject"
ID = "N33"
FEATURES = ["type.solaris-extended"]


def build(a):
    a.pax([(b"path", b"from-x")], typeflag=b"X", note="typeflag X, as Solaris tar wrote it")
    a.file(b"from-header", b"which name?\n")
    a.end()

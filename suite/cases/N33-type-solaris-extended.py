"""A Solaris extended header, typeflag `X`: a pax header, or a file?

The archive has a header of typeflag `X` named `PaxHeader` containing the pax record `path=from-x`,
followed by a file whose ustar header gives the name `from-header`.

Solaris tar writes extended headers with typeflag `X` instead of POSIX's `x`. Under POSIX,
typeflags `A` to `Z` are reserved for [custom implementations][custom-type], and a reader that does
not recognize one extracts it [as a regular file][unknown-type]. A reader that treats `X` as a pax
extended header extracts the file as `from-x`. A reader that treats `X` as an unknown regular file
extracts `PaxHeader` containing the record, followed by `from-header`, while one that skips unknown
typeflags extracts `from-header` alone.

Decision point: whether typeflag `X` is an extended header.
Seen in: none of the scanned tarballs.
See also: F16, an unknown typeflag with a size.
"""

VERDICT = "reject"
ID = "N33"
FEATURES = ["type.solaris-extended"]


def build(a):
    a.pax([(b"path", b"from-x")], typeflag=b"X", note="typeflag X, as Solaris tar writes it")
    a.file(b"from-header", b"which name?\n")
    a.end()

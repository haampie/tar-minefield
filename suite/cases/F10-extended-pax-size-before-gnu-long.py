"""A pax `size` followed by a GNU long name: which of them does the size apply to?

The archive has a pax header with `size=512`, then a GNU long name header with the name
`long-name`, then the member, whose header has the name `short-name` and the size 0, then an empty
file `smuggled`.

GNU's format does not say how the two extensions combine, and [POSIX][unknown-type] does not define
GNU long names: in POSIX, the long name header is a file of an unknown type, so the pax size applies
to it. This case is ambiguous because the size applies either to the long name header, and
`smuggled` is a member of its own, or to the member, whose data then takes in the header of
`smuggled`, or to both, so that the member has that data and `smuggled` is a member as well. A
reader that does not know GNU long names extracts the member as `short-name`. This is the bug class
of GHSA-3pv8-6f4r-ffg2 (tar-rs) and CVE-2026-53655 (node-tar).

Decision point: which header a pax size applies to, when another extended header follows.
Seen in: none of the scanned tarballs.
"""

VERDICT = "reject"
ID = "F10"
FEATURES = ['extended.pax-size-before-gnu-long']


def build(a):
    a.pax([(b"size", b"512")], note="size=512")
    a.gnu_long(b"long-name", note="the name of the next member")
    a.header(b"short-name", b"0", 0, note="size 0, but the pax size is 512")
    a.file(b"smuggled", b"", note="covered by the pax size, to some implementations")
    a.end()

"""A pax `size` followed by a GNU long name: which of them does the size apply to?

The archive has a pax header with `size=512`, a GNU long name header for `long-name`, a file header
named `short-name` with size 0, and finally an empty file `smuggled`.

GNU's format does not specify how pax headers and GNU long names interact, and [POSIX][unknown-type]
does not define GNU long names: to a pure POSIX reader, the typeflag `L` header is a file of unknown
type, so the pax `size` applies to it. A reader that applies `size=512` to the long name header
leaves `smuggled` as a separate member. A reader that applies `size=512` to the file member consumes
`smuggled`'s header as the file's data, while one that applies `size=512` to both gives the file
that data and still extracts `smuggled`. A reader that does not support GNU long names extracts the
file as `short-name`. This is the bug class of GHSA-3pv8-6f4r-ffg2 (tar-rs) and CVE-2026-53655
(node-tar).

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

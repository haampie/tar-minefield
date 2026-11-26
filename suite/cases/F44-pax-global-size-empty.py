"""An empty `size` in a global pax header: does it delete the size of every later member, or set it?

The archive has a global header (typeflag `g`) with the single record `size=`, followed by a file
`a` with size 512 in its ustar header, and then an empty file `smuggled`.

Under [POSIX][empty-value], an empty pax value deletes any header field of the same name, and a
global header value [applies][global] to all subsequent files. Read as deleting `a`'s size field
(whose ustar value is then [ignored][corresponding]), `size=` leaves `a` without a size. Read as
[assigning][g-assigned] an empty size to `a`, it gives size 0 (so `smuggled` is extracted as a
member). Read as clearing only an earlier global `size`, it leaves `a`'s ustar size of 512 intact
(consuming `smuggled`'s header as `a`'s data).

Decision point: what an empty size in a global header deletes.
Seen in: none of the scanned tarballs.
See also: F20, a size in a global header, and F21, an empty size in an extended header.
"""

VERDICT = "reject"
ID = "F44"
FEATURES = ["pax-global.empty-value.size"]


def build(a):
    a.pax([(b"size", b"")], typeflag=b"g", name=b"pax_global_header",
          note="size=, which deletes the size of every later member")
    a.header(b"a", b"0", 512, note="size 512")
    a.file(b"smuggled", b"", note="the data of a, to a reader that keeps its size")
    a.end()

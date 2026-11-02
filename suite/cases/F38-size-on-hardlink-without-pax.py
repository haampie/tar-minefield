"""A size in the header of a hard link, in an archive without pax headers: ustar or pax?

The archive has a file `a`, then a hard link `h` to `a`, with the size 512 in its header, then an
empty file `smuggled`. No header of the archive is a pax header.

The bytes are the same whether the archive is read as ustar or as pax, as the [physical
layout][same-layout] of pax is that of ustar, and a reader [detects][detected] the format. In ustar,
[no data][no-data] is stored for a hard link, so the block after the header of `h` is the header of
`smuggled`; in pax, [data][link-data] follows a hard link whose size is not zero, so that block is
the data of `h`. This case is ambiguous because nothing in the archive says which format it is: the
tree has `a` and `smuggled`, or `a` alone, as it is or with that block as its contents.

Decision point: whether a size in the header of a hard link applies, in an archive without pax
headers.
Seen in: none of the scanned tarballs.
See also: F34, the same in an archive with a pax header, which settles the format.
"""

VERDICT = "reject"
ID = "F38"
FEATURES = ["size.on-hardlink"]


def build(a):
    a.file(b"a", b"a\n")
    a.header(b"h", b"1", 512, note="a hard link to a, with a size of 512", linkname=b"a")
    a.file(b"smuggled", b"", note="the block that the size covers")
    a.end()

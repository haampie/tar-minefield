r"""A size in the header of a hardlink, in an archive without pax headers: ustar or pax?

The archive has a file `a`, a hardlink `h` to `a` with size 512 in its header, and an empty file
`smuggled`, with no pax headers.

Hardlink sizes follow different rules in ustar and pax. In ustar, a hardlink's size [must be
zero][link-size-zero] and the archive [does not store data][no-data] for it, making the block after
`h` the header of `smuggled`. In pax, a hardlink may carry [data blocks][link-data] and a non-zero
size, making that block `h`'s data. Although POSIX requires [automatic format detection][detected],
this archive matches both formats: pax uses the [same physical layout][same-layout] and magic as
ustar, and [extended headers are optional][extended-optional]. Read as ustar, the extracted tree has
`a`, `h` and `smuggled`; read as pax, it has only `a` and `h`.

Decision point: whether a size in the header of a hardlink applies, in an archive without pax
headers.
Seen in: none of the scanned tarballs.
See also: F34, the same in an archive with a pax header, which marks it as pax.
"""

VERDICT = "reject"
ID = "F38"
FEATURES = ["size.on-hardlink"]


def build(a):
    a.file(b"a", b"a\n")
    a.header(b"h", b"1", 512, note="a hardlink to a, with a size of 512", linkname=b"a")
    a.file(b"smuggled", b"", note="the block that the size covers")
    a.end()

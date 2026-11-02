r"""A size in the header of a hard link, in an archive without pax headers: ustar or pax?

The archive has a file `a`, then a hard link `h` to `a`, with the size 512 in its header, then an
empty file `smuggled`. It does not have a pax header.

POSIX says two incompatible things about the size of a hard link. In ustar, it [shall be
zero][link-size-zero], and the archive [does not store data][no-data] for a hard link, so the block
after the header of `h` is the header of `smuggled`. In pax, [data][link-data] follows a hard link
whose size is not zero, so that block is the data of `h`. A reader [detects][detected] the format,
but every ustar archive is also a valid pax archive: the [layout][same-layout] of pax is that of
ustar, both have the same magic, and a pax archive [need not have][extended-optional] a pax header.
This case is ambiguous because POSIX contradicts itself: read as ustar, the tree has `a`, its link
`h` and `smuggled`; read as pax, it has `a` and `h` alone, which hold `a\n` or that block.

Decision point: whether a size in the header of a hard link applies, in an archive without pax
headers.
Seen in: none of the scanned tarballs.
See also: F34, the same in an archive with a pax header, which marks it as pax.
"""

VERDICT = "reject"
ID = "F38"
FEATURES = ["size.on-hardlink"]


def build(a):
    a.file(b"a", b"a\n")
    a.header(b"h", b"1", 512, note="a hard link to a, with a size of 512", linkname=b"a")
    a.file(b"smuggled", b"", note="the block that the size covers")
    a.end()

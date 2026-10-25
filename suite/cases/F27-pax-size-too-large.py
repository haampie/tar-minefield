"""A pax `size` of 2^64 + 512, which wraps around to 512 in 64 bits.

pax numbers can be of any length, but implementations keep sizes in 64 bits. In POSIX, the size is
2^64 + 512, which runs past the end of the archive. Read leniently, this case is ambiguous because
the size is 512, wrapped around, the header's, 0, or 2^64 - 1, clamped. With 512 the next block is
the data of `a`, with 0 the header of `smuggled`, and with 2^64 - 1 the data runs past the end of
the archive.

Decision point: what a pax number too large for the reader means.
Seen in: no source tarball.
"""

VERDICT = "reject"
ID = "F27"
FEATURES = ["pax.size-too-large"]


def build(a):
    a.pax([(b"size", b"%d" % (2**64 + 512))], note="size=2^64+512, for a")
    a.header(b"a", b"0", 0, note="size 0")
    a.file(b"smuggled", b"", note="the data of a, to an implementation that wraps the size to 512")
    a.end()

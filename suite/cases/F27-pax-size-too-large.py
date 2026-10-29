"""A pax `size` of 2^64 + 512, which wraps around to 512 in 64 bits.

The archive has a file `a`, whose pax header has the size 2^64 + 512 and whose header has the size
0, then an empty file `smuggled`.

pax numbers can be of any length, but many implementations keep sizes in 64 bits. In
[POSIX][size-decimal], the size is 2^64 + 512, which runs past the end of the archive. Read
leniently, this case is ambiguous because the size is also the header's, 0, with the pax size
discarded, which makes the next block the header of `smuggled`, or 512, wrapped around in 64 bits,
which makes it the data of `a`. Neither is a reading of POSIX, which takes the size as it is, and
the header's size is to be [ignored][corresponding] once a `size` record is there.

Decision point: what a pax number too large for the reader means.
Seen in: none of the scanned tarballs.
"""

VERDICT = "reject"
ID = "F27"
FEATURES = ["pax.size-too-large"]


def build(a):
    a.pax([(b"size", b"%d" % (2**64 + 512))], note="size=2^64+512, for a")
    a.header(b"a", b"0", 0, note="size 0")
    a.file(b"smuggled", b"", note="the data of a, to an implementation that wraps the size to 512")
    a.end()

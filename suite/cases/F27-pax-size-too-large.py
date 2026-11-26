"""A pax `size` of 2^64 + 512, which wraps around to 512 in 64 bits.

The archive has a file `a` with a pax `size` of 2^64 + 512 and a ustar size of 0, followed by an
empty file `smuggled`.

In [POSIX][size-decimal], a pax size can have any number of decimal digits, so the size is 2^64 +
512, which extends past the end of the archive. Many implementations store file sizes in a 64-bit
integer: wrapping 2^64 + 512 modulo 2^64 yields 512 and consumes the next block as `a`'s data,
whereas discarding the overflowing pax record and falling back to the ustar size of 0 (contrary to
POSIX, which requires [ignoring][corresponding] the ustar size) treats the next block as
`smuggled`'s header.

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

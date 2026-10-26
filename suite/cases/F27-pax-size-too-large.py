"""A pax `size` of 2^64 + 512, which wraps around to 512 in 64 bits.

pax numbers can be of any length, but many implementations keep sizes in 64 bits. In POSIX, the
size is 2^64 + 512, which runs past the end of the archive, as Python's `tarfile` and node-tar read
it. Read leniently, this case is ambiguous because BusyBox, 7-Zip, PharData, Rust's tar, RubyGems,
Archive::Tar and Haskell's tar take the header's size, 0, instead, and extract the next block as a
file `smuggled`. Wrapped around to 512 in 64 bits, the next block would be the data of `a`.

Decision point: what a pax number too large for the reader means.
Seen in: none of the scanned tarballs.
"""

VERDICT = "reject"
ID = "F27"
FEATURES = ["pax.size-too-large"]
POSIX = "size-decimal"


def build(a):
    a.pax([(b"size", b"%d" % (2**64 + 512))], note="size=2^64+512, for a")
    a.header(b"a", b"0", 0, note="size 0")
    a.file(b"smuggled", b"", note="the data of a, to an implementation that wraps the size to 512")
    a.end()

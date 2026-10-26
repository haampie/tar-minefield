"""A base-256 size of 2^64 + 512 in the header, which wraps around to 512 in 64 bits.

A base-256 number has 11 bytes, 88 bits, after its first byte, 0x80, but many implementations keep
sizes in 64 bits. The whole number, 2^64 + 512, runs past the end of the archive. Read leniently,
this case is ambiguous because its low 64 bits are 512, which makes the next block the data of `a`;
a reader that skips the header instead extracts the next block as a file `smuggled`, without `a`.

Decision point: what a size too large for the reader means.
Seen in: none of the scanned tarballs.
"""

VERDICT = "reject"
ID = "F30"
FEATURES = ["number.size.base256-too-large"]


def build(a):
    a.header(b"a", b"0", size=b"\x80" + (2**64 + 512).to_bytes(11, "big"),
             note="size 2^64+512, in base 256")
    a.file(b"smuggled", b"", note="the data of a, to an implementation that keeps the low 64 bits")
    a.end()

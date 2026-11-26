"""A base-256 size of 2^64 + 512 in the header, which wraps around to 512 in 64 bits.

The archive has a file `a` whose size field encodes 2^64 + 512 in base 256, followed by an empty
file `smuggled`.

After the leading `0x80` marker byte, a base-256 size field holds 11 bytes (88 bits), whereas many
implementations store sizes in a 64-bit integer. The full 88-bit value extends past the end of the
archive, but a reader that truncates it to the low 64 bits gets 512 and consumes the next block as
`a`'s data. A reader that skips `a`'s header as invalid instead extracts `smuggled` without `a`.

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

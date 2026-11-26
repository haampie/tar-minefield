"""A negative base-256 size in the header, -512, which a member cannot have.

The archive has a file `a` whose size field encodes -512 in base 256, followed by an empty file
`smuggled`.

GNU tar encodes numbers that do not fit in octal using two's-complement base 256, with `0x80` in the
first byte for positive values and `0xff` for negative values. Although a negative file size is
meaningless, the format can represent it. A lenient reader might clamp or default the negative size
to 0 (reading the next block as `smuggled`'s header), drop the sign and use 512 (consuming the next
block as `a`'s data), or interpret the bytes as an unsigned number running past the end of the
archive.

Decision point: whether a size may be negative, and what a negative one means.
Seen in: none of the scanned tarballs.
"""

VERDICT = "reject"
ID = "F29"
FEATURES = ["number.size.base256-negative"]


def build(a):
    a.header(b"a", b"0", size=b"\xff" + (256**11 - 512).to_bytes(11, "big"),
             note="size -512, in base 256")
    a.file(b"smuggled", b"", note="a member, unless a reading of the size covers it")
    a.end()

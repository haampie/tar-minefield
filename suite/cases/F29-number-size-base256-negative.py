"""A negative base-256 size in the header, -512, which a member cannot have.

The archive has a file `a`, whose size field is -512 in base 256, then an empty file `smuggled`.

GNU tar writes numbers too large for octal in base 256: the first byte of the field is `0x80` for a
positive number, and `0xff` for a negative one, in two's complement. A negative size is meaningless,
but the encoding allows it. Read leniently, this case is ambiguous because the size is either 0 (and
the next block is the header of `smuggled`), or 512 without its sign (and the next block is the data
of `a`), or the field read as an unsigned number (which runs past the end of the archive).

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

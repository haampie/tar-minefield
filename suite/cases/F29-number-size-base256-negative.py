"""A negative base-256 size in the header, -512, which no member can have.

GNU tar writes numbers too large for octal in base 256: the first byte of the field is 0x80 for a
positive number, and 0xff for a negative one, in two's complement. A negative size is meaningless,
but the encoding allows it. Read leniently, this case is ambiguous because the size is 0, 512
without its sign, or the field read as an unsigned number. With 0 the next block is the header of
`smuggled`, with 512 the data of `a`, and the unsigned number runs past the end of the archive.

Decision point: whether a size may be negative, and what a negative one means.
Seen in: no source tarball.
"""

VERDICT = "reject"
ID = "F29"
FEATURES = ["number.size.base256-negative"]


def build(a):
    a.header(b"a", b"0", size=b"\xff" + (256**11 - 512).to_bytes(11, "big"),
             note="size -512, in base 256")
    a.file(b"smuggled", b"", note="a member, unless a reading of the size covers it")
    a.end()

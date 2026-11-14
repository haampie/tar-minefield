"""A size whose first byte is `0x81`: base-256, or not a number?

The archive has a file `a`, whose size field is the byte `0x81`, followed by 512 as a binary number
of 11 bytes, then an empty file `smuggled`.

In GNU's format, a number in base-256 starts with the byte `0x80`, and a negative one with `0xff`.
In [POSIX][zero-filled], numeric fields are octal, so base-256 is an extension, and what any other
first byte over `0x7f` means is not specified. Read leniently, this case is ambiguous because a
reader can read the size in one of four ways. A reader that tells base-256 apart from octal by the
high bit of the first byte, and drops the rest of that byte, reads 512, and the next block is the
data of `a`. One that keeps the other bits of the first byte reads a size far past the end of the
archive. One that reads octal digits reads 0, as the field does not have any, and the next block is
the header of `smuggled`. One that skips the block, as it does with a block that is not a header,
extracts `smuggled` alone, without an error.

Decision point: which first bytes make a numeric field base-256.
Seen in: none of the scanned tarballs.
See also: F56, a size in base-256, and F30, a base-256 size that wraps around.
"""

VERDICT = "reject"
ID = "F71"
FEATURES = ["number.size.invalid-character"]


def build(a):
    a.header(b"a", b"0", b"\x81" + (512).to_bytes(11, "big"), note="size 512, or 0, or 2^88 + 512")
    a.file(b"smuggled", b"", note="the data of a, to a reader that takes 0x81 for base-256")
    a.end()

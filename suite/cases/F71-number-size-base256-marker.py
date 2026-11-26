"""A size field starting with `0x81`: base-256, or invalid?

The archive has a file `a` whose size field starts with `0x81` followed by 512 as an 11-byte
big-endian integer, then an empty file `smuggled`.

In GNU's base-256 extension, positive numbers start with `0x80` and negative numbers with `0xff`.
Standard [POSIX][zero-filled] numeric fields are octal, and other leading bytes above `0x7f` are
undefined. A reader that checks only the high bit and masks off the rest of the first byte reads a
size of 512, consuming the next block as `a`'s data. A reader that includes the low bit of `0x81` in
the value reads a size of 2^88 + 512, far past the end of the archive. A reader that expects octal
digits finds none, takes the size as 0, and reads the next block as `smuggled`'s header. Finally, a
reader that skips `a`'s header as invalid extracts `smuggled` alone.

Decision point: which leading bytes mark a base-256 numeric field.
Seen in: none of the scanned tarballs.
See also: F56, a size in base-256, and F30, a base-256 size that wraps around.
"""

VERDICT = "reject"
ID = "F71"
FEATURES = ["number.size.invalid-character"]


def build(a):
    a.header(b"a", b"0", b"\x81" + (512).to_bytes(11, "big"), note="size 512, 0, or 2^88 + 512")
    a.file(b"smuggled", b"", note="a's data if 0x81 is read as base-256")
    a.end()

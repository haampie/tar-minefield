"""A size field starting with a minus sign.

The archive has a file `a` with `-0000001000` in its size field, followed by an empty file
`smuggled`.

In [POSIX][zero-filled], numeric fields are unsigned octal numbers filled with leading zeros. If a
lenient reader skips the minus sign, the size is octal 1000 (512) and the next block becomes `a`'s
data. If the reader stops at the sign, the size is 0 and the next block is `smuggled`'s header.

Decision point: whether a numeric field may have a sign.
Seen in: none of the scanned tarballs.
See also: F51, a size with a plus sign, and F29, a negative size in base-256.
"""

VERDICT = "reject"
ID = "F70"
FEATURES = ["number.size.invalid-character"]


def build(a):
    a.header(b"a", b"0", b"-0000001000\0", note="size 512 or 0")
    a.file(b"smuggled", b"", note="a's data if the minus sign is skipped")
    a.end()

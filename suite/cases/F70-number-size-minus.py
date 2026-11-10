"""A size with a minus sign, `-0000001000`.

The archive has a file `a`, whose size field is `-0000001000`, then an empty file `smuggled`.

In [POSIX][zero-filled], numeric fields are octal numbers filled with leading zeros, without a sign,
and a size is not negative. Read leniently, this case is ambiguous because the size is either 512,
octal 1000, if the sign is dropped (and the next block is the data of `a`), or 0, if the number ends
at the sign (and the next block is the header of `smuggled`).

Decision point: whether a numeric field may have a sign.
Seen in: none of the scanned tarballs.
See also: F51, a size with a plus sign, and F29, a negative size in base-256.
"""

VERDICT = "reject"
ID = "F70"
FEATURES = ["number.size.invalid-character"]


def build(a):
    a.header(b"a", b"0", b"-0000001000\0", note="size 512, or 0")
    a.file(b"smuggled", b"", note="the data of a, to a reader that drops the sign")
    a.end()

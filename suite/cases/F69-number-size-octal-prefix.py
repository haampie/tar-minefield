"""A size with the prefix `0o`, `0o000001000`.

The archive has a file `a`, whose size field is `0o000001000`, then an empty file `smuggled`.

In [POSIX][zero-filled], numeric fields are octal numbers filled with leading zeros, and `o` is not
a digit. Read leniently, this case is ambiguous because a reader can take the size in one of two
ways. A reader that accepts `0o` as the prefix of an octal number when it converts the field to a
number, as Python's `int` does, reads 512, octal 1000 (and the next block is the data of `a`). One
that ends the number at the `o` reads 0 (and the next block is the header of `smuggled`).

Decision point: how a numeric field with a letter is read.
Seen in: none of the scanned tarballs.
See also: F37, a size with the digit 9, and F51, a size with a plus sign.
"""

VERDICT = "reject"
ID = "F69"
FEATURES = ["number.size.invalid-character"]


def build(a):
    a.header(b"a", b"0", b"0o000001000\0", note="size 512, or 0")
    a.file(b"smuggled", b"", note="the data of a, to a reader that takes 0o for a prefix")
    a.end()

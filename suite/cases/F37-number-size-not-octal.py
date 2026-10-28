"""A size with the digit 9, which is not octal.

The size field is `00000000090`. In POSIX, numeric fields are octal numbers filled with leading
zeros, and 9 is not an octal digit. Read leniently, this case is ambiguous because the size is
either 0, if the number ends before the 9 (and the next block is the header of `smuggled`), or 72,
9 × 8, if the 9 is taken as a digit (and the next block is the data of `a`).

Decision point: how a numeric field with a digit that is not octal is read.
Seen in: none of the scanned tarballs.
"""

VERDICT = "reject"
ID = "F37"
FEATURES = ['number.size.invalid-character']
POSIX = "zero-filled"


def build(a):
    a.header(b"a", b"0", b"00000000090\0", note="size 0 or 72")
    a.file(b"smuggled", b"", note="the data of a, to an implementation that takes 9 as a digit")
    a.end()

"""A pax `size` with an underscore, `5_12`, which some conversions of strings to numbers accept.

The archive has a file `a`, whose pax header has `size=5_12` and whose header has the size 0, then
an empty file `smuggled`.

In [POSIX][size-decimal], a pax size is a decimal number. Read leniently, this case is ambiguous
because a reader can read the size in one of three ways. A reader that takes the underscore for a
separator of digits reads 512, and the next block is the data of `a`. One that ends the number at
the underscore reads 5, and `a` is the first 5 bytes of the next block. One that keeps the size of
the header reads 0, and the next block is the header of `smuggled`.

Decision point: how a pax size that is not a decimal number is read.
Seen in: none of the scanned tarballs.
See also: F23, F24 and F25, a pax size with a plus sign, with a leading space, and with digits that
are not ASCII.
"""

VERDICT = "reject"
ID = "F50"
FEATURES = ["pax.invalid-size"]


def build(a):
    a.pax([(b"size", b"5_12")], note="size=5_12, for a")
    a.header(b"a", b"0", 0, note="size 0")
    a.file(b"smuggled", b"", note="the data of a, to an implementation that reads 512")
    a.end()

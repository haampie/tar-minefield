"""A pax `size` with an underscore, `5_12`, which some conversions of strings to numbers accept.

The archive has a file `a`, whose pax header has `size=5_12` and whose header has the size 0, then
an empty file `smuggled`.

In [POSIX][size-decimal], a pax size is a decimal number. Read leniently, this case is ambiguous
because the size is either 512, if the underscore is taken for a separator of digits (and the next
block is the data of `a`), 5, if the number ends at the underscore (and `a` is the first 5 bytes of
the next block), or 0, as the header specifies (and the next block is the header of `smuggled`).

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

"""A pax `size` with a decimal point, `512.0`.

The archive has a file `a`, whose pax header has `size=512.0` and whose header has the size 0, then
an empty file `smuggled`.

In [POSIX][size-decimal], a pax size is decimal digits, without a decimal point. The values of pax
records that can have a decimal point are the [times][time-decimal]. Read leniently, this case is
ambiguous because a reader that reads every number of a pax record as it reads a time, or that ends
the number at the point, reads 512 (and the next block is the data of `a`), and one that does not
take the value for a number keeps the size of the header, 0 (and the next block is the header of
`smuggled`).

Decision point: how a pax size that is not a decimal number is read.
Seen in: none of the scanned tarballs.
See also: F50, a pax size with an underscore, and F23, a pax size with a plus sign.
"""

VERDICT = "reject"
ID = "F75"
FEATURES = ["pax.invalid-size"]


def build(a):
    a.pax([(b"size", b"512.0")], note="a size with a decimal point")
    a.header(b"a", b"0", 0)
    a.file(b"smuggled", b"", note="the data of a, to a reader that reads 512")
    a.end()

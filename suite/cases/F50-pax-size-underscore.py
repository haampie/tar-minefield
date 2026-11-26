"""A pax `size` with an underscore, `5_12`, which some conversions of strings to numbers accept.

The archive has a file `a` with `size=5_12` in its pax header and size 0 in its ustar header,
followed by an empty file `smuggled`.

In [POSIX][size-decimal], a pax size is an integer in decimal digits. A reader whose number parser
allows underscores as digit separators (such as Python's `int`) reads 512 and consumes the next
block as `a`'s data. A reader that stops parsing at the underscore reads a size of 5 and extracts
the first 5 bytes of the next block as `a`. A reader that ignores the invalid pax `size` falls back
to the ustar size of 0 and reads the next block as `smuggled`'s header.

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

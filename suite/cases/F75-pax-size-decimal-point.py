"""A pax `size` with a decimal point: `512.0`.

The archive has a file `a` with `size=512.0` in its pax header and size 0 in its ustar header,
followed by an empty file `smuggled`.

A [POSIX][size-decimal] pax size is an integer in decimal digits; only [timestamp
records][time-decimal] allow a decimal point. A reader that parses all numeric pax values like
timestamps, or stops at the decimal point, uses a size of 512 and consumes the next block as `a`'s
data. A reader that ignores the non-integer pax `size` falls back to the ustar size of 0 and reads
the next block as `smuggled`'s header.

Decision point: how a non-integer pax `size` is handled.
Seen in: none of the scanned tarballs.
See also: F50, a pax size with an underscore, and F23, a pax size with a plus sign.
"""

VERDICT = "reject"
ID = "F75"
FEATURES = ["pax.invalid-size"]


def build(a):
    a.pax([(b"size", b"512.0")], note="size=512.0")
    a.header(b"a", b"0", 0)
    a.file(b"smuggled", b"", note="a's data if size is 512")
    a.end()

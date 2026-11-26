"""A pax `size` with a plus sign, `+512`, which conversions of strings to numbers accept.

The archive has a file `a` with `size=+512` in its pax header and size 0 in its ustar header,
followed by an empty file `smuggled`.

In [POSIX][size-decimal], a pax size consists of decimal digits without a sign. Read leniently,
standard number parsers such as Python's `int`, Go's `strconv.ParseInt` and Rust's `u64::from_str`
accept a leading `+` and parse `+512` as 512, consuming the next block as `a`'s data, while a reader
that rejects `+512` and falls back to the ustar size of 0 reads the next block as `smuggled`'s
header. Neither follows from POSIX, which does not say what a `size` record that is not a decimal
number means.

Decision point: whether a pax size may have a sign.
Seen in: none of the scanned tarballs.
"""

VERDICT = "reject"
ID = "F23"
FEATURES = ["pax.invalid-size"]


def build(a):
    a.pax([(b"size", b"+512")], note="size=+512, for a")
    a.header(b"a", b"0", 0, note="size 0")
    a.file(b"smuggled", b"", note="the data of a, to an implementation that reads +512 as 512")
    a.end()

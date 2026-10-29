"""A pax `size` with a plus sign, `+512`, which conversions of strings to numbers accept.

The archive has a file `a`, whose pax header has `size=+512` and whose header has the size 0, then
an empty file `smuggled`.

In [POSIX][size-decimal], a pax size is decimal digits, without a sign. But the conversions of
strings to numbers that implementations use, such as Python's `int`, Go's `strconv.ParseInt` and
Rust's `u64::from_str`, read `+512` as 512. Read leniently, this case is ambiguous because the size
is either 512, as read that way (and the next block is the data of `a`), or 0, as the header
specifies (and the next block is the header of `smuggled`). Neither is a reading of POSIX: `+512` is
not a pax size, and the header's size is to be [ignored][corresponding] once a `size` record is
there.

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

"""A pax `size` with a leading space, ` 512`, which conversions of strings to numbers skip.

The archive has a file `a` with `size= 512` in its pax header and size 0 in its ustar header,
followed by an empty file `smuggled`.

In a pax record `<length> <key>=<value>\\n`, the value begins immediately after `=`, so here the
value starts with a space. Under [POSIX][size-decimal], a pax size contains only decimal digits.
Read leniently, number parsers such as Python's `int` and C's `strtoull` skip leading whitespace and
return 512, consuming the next block as `a`'s data, while a reader that rejects the space-prefixed
pax value and falls back to the ustar size of 0 reads the next block as `smuggled`'s header. Neither
follows from POSIX, which does not say what a `size` record that is not a decimal number means.

Decision point: whether a pax size may have whitespace.
Seen in: none of the scanned tarballs.
"""

VERDICT = "reject"
ID = "F24"
FEATURES = ["pax.invalid-size"]


def build(a):
    a.pax([(b"size", b" 512")], note="size= 512, for a")
    a.header(b"a", b"0", 0, note="size 0")
    a.file(b"smuggled", b"", note="the data of a, to an implementation that skips the space")
    a.end()

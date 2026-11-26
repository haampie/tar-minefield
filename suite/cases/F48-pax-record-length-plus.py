"""A pax record whose length has a plus sign, `+17`.

The archive has a file with a single 17-byte pax record, `+17 path=renamed` followed by a newline,
and `header-name` in its ustar name field.

In POSIX, a pax record's [length][record-length] is formatted as an unsigned decimal integer (`%d`)
without a leading sign. A lenient reader that accepts `+17` as 17 applies `path=renamed`, whereas
one that ignores the malformed record or discards the pax header falls back to `header-name`.

Decision point: whether the length of a pax record may have a sign.
Seen in: none of the scanned tarballs.
See also: F23, a pax size with a plus sign, and F36, a record length that is one short.
"""

VERDICT = "reject"
ID = "F48"
FEATURES = ["pax.invalid-length"]

RECORD = b"+17 path=renamed\n"


def build(a):
    a.header(b"PaxHeader", b"x", len(RECORD), note="one record, whose length has a plus sign")
    a.raw(RECORD, "data: a pax record of 17 bytes")
    a.file(b"header-name", b"which name?\n")
    a.end()

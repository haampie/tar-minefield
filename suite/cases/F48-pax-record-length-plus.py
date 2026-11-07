"""A pax record whose length has a plus sign, `+17`.

The archive has a file whose pax header has one record, `+17 path=renamed`, followed by a newline,
which is 17 bytes, and whose header has the name `header-name`.

In POSIX, the [length][record-length] of a pax record is its decimal length in octets, as `%d`
writes it, without a sign. Read leniently, this case is ambiguous because the record is either
`path=renamed`, and the file is `renamed`, or no record, and the file is `header-name`, to a reader
that ignores the record or the whole extended header.

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

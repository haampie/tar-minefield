"""An empty line between two pax records.

The archive has a file whose pax header has the record `comment=x`, followed by a newline,
followed by the record `path=renamed`. Its header has the name `header-name`.

In POSIX, an extended header [consists of records][records], each of which starts with its
[length][record-length], so a newline between two of them is not a record. This case is ambiguous
because a reader that skips the empty line reads `path=renamed`, and the file is `renamed`; one
that stops there, or ignores the extended header, keeps `header-name`; and one that takes the
newline for the start of the next record reads its length from one byte too early, and cuts the
name to `rename`.

Decision point: whether a pax header may have bytes between its records.
Seen in: none of the scanned tarballs.
See also: F36, a record length that is one short.
"""

VERDICT = "reject"
ID = "F50"
FEATURES = ["pax.invalid-length"]

RECORDS = b"13 comment=x\n\n16 path=renamed\n"


def build(a):
    a.header(b"PaxHeader", b"x", len(RECORDS), note="two records, with a newline between them")
    a.raw(RECORDS, "data: a comment, an empty line, and a path")
    a.file(b"header-name", b"which name?\n")
    a.end()

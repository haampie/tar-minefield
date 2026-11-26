"""An empty line between two pax records.

The archive has a file whose pax header contains `comment=x`, an extra newline, and `path=renamed`.
The file's ustar header gives the name `header-name`.

A POSIX extended header [consists of records][records] that each begin with a decimal
[byte length][record-length], leaving no room for blank lines between records. A reader that skips
the blank line applies `path=renamed`. A reader that stops parsing at the blank line or discards the
pax header extracts `header-name`. A reader that advances by the declared length plus one extra byte
starts reading the second record one byte late and truncates the name to `rename`.

Decision point: whether a pax header may have bytes between its records.
Seen in: none of the scanned tarballs.
See also: F36, a record length that is one short.
"""

VERDICT = "reject"
ID = "F49"
FEATURES = ["pax.invalid-length"]

RECORDS = b"13 comment=x\n\n16 path=renamed\n"


def build(a):
    a.header(b"PaxHeader", b"x", len(RECORDS), note="two records, with a newline between them")
    a.raw(RECORDS, "data: a comment, an empty line, and a path")
    a.file(b"header-name", b"which name?\n")
    a.end()

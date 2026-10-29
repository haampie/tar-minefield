"""A pax record whose length is one byte short, so that it ends just before its newline.

The archive has a pax header with one record, `16 path=from-pax` followed by a newline, which is 17
bytes, although its length says 16; then the member, whose header has the name `from-header`.

In [POSIX][record-length], the length of a record counts every byte of it, its newline included, so
the record is malformed. This case is ambiguous in practice because only a reader that delimits the
record by its length, and checks that it ends in a newline, recognizes it as malformed: one that
splits records on newlines, or does not check, takes it for a valid record.

Decision point: whether a pax record whose length does not end at its newline is recognized as
malformed.
Seen in: none of the scanned tarballs.
See also: F28, a newline inside a value.
"""

VERDICT = "reject"
ID = "F36"
FEATURES = ["pax.invalid-length", "pax.no-newline"]

RECORD = b"16 path=from-pax\n"


def build(a):
    a.header(b"PaxHeader", b"x", len(RECORD), note="one record, whose length is one short")
    a.raw(RECORD, "data: a pax record of 17 bytes that says it has 16")
    a.file(b"from-header", b"which name?\n")
    a.end()

"""A pax record whose length is one less than its size, so that it does not end in a newline.

The extended header holds one record, `16 path=from-pax` and a newline, which is 17 bytes. Taken at
its word, the record is 16 bytes, its value `from-pa`, and it does not end in a newline; the byte
after it, the newline, is not a record. POSIX says that the length is the length of the record,
including its newline, so the record is malformed. This case is ambiguous in practice because the
record is applied as its length says, with the name `from-pa`, or as its newline says, with the
name `from-pax`, or dropped, so that the member keeps the name of its header, `from-header`.

Decision point: whether a pax record is delimited by its length or by its newline, when they
disagree.
Seen in: none of the scanned tarballs.
See also: F28, a newline inside a value.
"""

VERDICT = "reject"
ID = "F36"
FEATURES = ["pax.invalid-length", "pax.no-newline"]
POSIX = "record-length"

RECORD = b"16 path=from-pax\n"


def build(a):
    a.header(b"PaxHeader", b"x", len(RECORD), note="one record, whose length is one short")
    a.raw(RECORD, "data: a pax record of 17 bytes that says it has 16")
    a.file(b"from-header", b"which name?\n")
    a.end()

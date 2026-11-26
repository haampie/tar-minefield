"""A pax record whose length is one byte short, so that it ends just before its newline.

The archive has a pax header with a single 17-byte record, `16 path=from-pax` followed by a newline,
whose declared length is 16, followed by a file whose ustar header gives the name `from-header`.

Under [POSIX][record-length], a pax record's length includes every byte through its trailing
newline, making this record malformed. Only a reader that frames the record by its declared length
and checks for the trailing newline detects the error; one that splits records on newlines or does
not check the trailing byte accepts `path=from-pax`.

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

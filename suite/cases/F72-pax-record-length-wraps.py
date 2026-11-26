"""A pax record length of 2^32 + 24, which wraps to 24 in 32-bit arithmetic.

The archive has a 24-byte pax payload containing a single record, `4294967320 path=renamed`,
followed by a newline. Its declared length of 4294967320 equals 2^32 + 24. The following file header
has the name `header-name`.

In [POSIX][record-length], a pax record's length gives its byte count, which here exceeds the pax
header's 24-byte payload. A reader that stores the length in a 32-bit integer wraps it to 24,
matches the record boundary, and extracts `renamed`. A reader that parses the full integer sees a
record extending past the pax header: it either reports an error, drops the record and extracts
`header-name`, or takes the rest of the payload as the value and extracts `renamed` with a trailing
newline.

Decision point: whether a pax record whose length runs past its header is recognized as malformed.
Seen in: none of the scanned tarballs.
See also: F36, a pax record whose length is one byte short, and F30, a base-256 size that wraps
around.
"""

VERDICT = "reject"
ID = "F72"
FEATURES = ["pax.invalid-length"]
RECORD = b"4294967320 path=renamed\n"
assert len(RECORD) == 24


def build(a):
    a.header(b"PaxHeader", b"x", len(RECORD), note="record length 2^32 + 24")
    a.raw(RECORD, "data: a pax record of 24 bytes that says it has 4294967320")
    a.file(b"header-name", b"which name?\n")
    a.end()

"""A pax record whose length is 2^32 + 24, which wraps around to 24 in 32 bits.

The archive has a pax header of 24 bytes with one record, `4294967320 path=renamed` followed by a
newline. Its length says 4294967320, which is 2^32 + 24, and the record has 24 bytes. After it is
the member, whose header has the name `header-name`.

In [POSIX][record-length], the length of a record counts its bytes, and this one says that the
record is longer than its header. This case is ambiguous in practice because a reader that keeps the
length in 32 bits reads 24, which is where the record ends, and extracts `renamed`. One that reads
the whole number finds a record that runs past the end of the header: it reports an error, or drops
the record and extracts `header-name`, or takes the rest of the header for the value, and extracts a
file whose name is `renamed`, followed by a newline.

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
    a.header(b"PaxHeader", b"x", len(RECORD), note="one record, whose length is 2^32 too large")
    a.raw(RECORD, "data: a pax record of 24 bytes that says it has 4294967320")
    a.file(b"header-name", b"which name?\n")
    a.end()

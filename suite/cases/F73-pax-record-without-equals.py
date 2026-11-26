"""A pax record without `=`, before a `path` record.

The archive has a file with two pax records: `11 comment` (followed by a newline, with no equals
sign) and `path=renamed`. The file's ustar header gives the name `header-name`.

Every POSIX extended header [record][records] has the form `<length> <key>=<value>` followed by a
newline, making the first record malformed. Because records are framed by their [byte
length][record-length], a parser can still locate the next record. A reader that skips the malformed
record applies `path=renamed`, whereas one that stops parsing the pax header at the bad record falls
back to `header-name`. Other readers report an error.

Decision point: whether a reader skips a pax record without `=`, stops at it, or reports an error.
Seen in: none of the scanned tarballs.
See also: F36, a pax record whose length is one byte short.
"""

VERDICT = "reject"
ID = "F73"
FEATURES = ["pax.no-equals"]
RECORDS = b"11 comment\n" + b"16 path=renamed\n"


def build(a):
    a.header(b"PaxHeader", b"x", len(RECORDS), note="a record without =, then a path")
    a.raw(RECORDS, "data: pax records, of which the first does not have =")
    a.file(b"header-name", b"which name?\n")
    a.end()

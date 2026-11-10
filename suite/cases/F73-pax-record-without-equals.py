"""A pax record without `=`, before a `path` record.

The archive has a file whose pax header has two records. The first is `11 comment`, followed by a
newline, which does not have an equals sign. The second is `path=renamed`. The header of the file
has the name `header-name`.

In POSIX, an extended header consists of [records][records], and a record is `<length>
<key>=<value>`, followed by a newline, so the first record is malformed. Records are delimited by
their [length][record-length], so a reader can skip it. This case is ambiguous in practice because a
reader can take the header in one of three ways. A reader that skips the malformed record applies
the `path`, and extracts `renamed`. One that stops reading records at the malformed one, without an
error, extracts `header-name`. Other readers report an error.

Decision point: whether a pax record without `=` is skipped, is the last one that is read, or is an
error.
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

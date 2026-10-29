r"""A newline in a pax `path`, which split on lines is another record.

The archive has one file, `plain`, whose pax header has one record: a `path` with a newline in it,
`good\n1 path=evil`.

pax records are delimited by their length, so a value can contain a newline, and in
[POSIX][record-length] the path is `good\n1 path=evil`. Split on lines instead, the extended header
has a second record, `path=evil`, and the path is `good` or `evil`. This case is ambiguous in
practice because a reader that discards the records as malformed extracts the header's name,
`plain`.

Decision point: whether a pax record is delimited by its length or by a newline.
Seen in: none of the scanned tarballs. Newlines in pax values are only in xattrs, such as Minion
10.31, which the default policy accepts as xattrs are not extracted.
"""

VERDICT = "reject"
ID = "F13"
FEATURES = ['pax.newline-in-value.path']


def build(a):
    a.pax([(b"path", b"good\n1 path=evil")], note="a path with a newline")
    a.file(b"plain", b"which name?\n")
    a.end()

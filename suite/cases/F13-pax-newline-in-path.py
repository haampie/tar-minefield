r"""A newline in a pax `path`, which split on lines is another record.

pax records are delimited by their length, so a value can contain a newline, and in POSIX the path
is `good\n1 path=evil`. Split on lines instead, the extended header has a second record,
`path=evil`. This case is ambiguous in practice because the path is then `good` or `evil`, or, with
the records discarded as malformed, the header's name, `plain`.

Decision point: whether a pax record is delimited by its length or by a newline.
Seen in: no source tarball. Newlines in pax values are only in xattrs, such as Minion
10.31, which the default policy accepts as xattrs are not extracted.
"""

VERDICT = "reject"
ID = "F13"
FEATURES = ['pax.newline-in-value.path']
POSIX = "record-length"


def build(a):
    a.pax([(b"path", b"good\n1 path=evil")], note="a path with a newline")
    a.file(b"plain", b"which name?\n")
    a.end()

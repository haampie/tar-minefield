r"""A newline in a pax `path`, which split on lines is another record.

The archive has one file, `plain`, whose pax header has a single `path` record containing a newline:
`good\n1 path=evil`.

Because pax records are delimited by their [byte length][record-length], a value can contain a
newline, making the POSIX path `good\n1 path=evil`. A reader that splits the pax payload on newlines
instead sees a second record, `path=evil`, and extracts either `good` or `evil`. A reader that
discards the records as malformed falls back to the ustar header's name, `plain`.

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

r"""A newline in a pax `comment`, which split on lines leaves a `size` record.

The archive has a file `a`, whose header has the size 0 and whose pax header has one record, a
`comment` with a newline in it, `x\n12 size=512`, then an empty file `smuggled`.

pax records are delimited by their length, so a value can contain a newline, and in [POSIX][comment]
every comment is ignored, so `a` has the size in its header, which is 0, and the next block is the
header of `smuggled`. Split on lines, the extended header has a second record, `size=512`. This case
is ambiguous in practice because, read that way, the block is the data of `a`.

Decision point: whether a pax record is delimited by its length or by a newline.
Seen in: none of the scanned tarballs. Newlines in pax values are only in xattrs, such as Minion
10.31, which the default policy accepts as xattrs are not extracted.
"""

VERDICT = "reject"
ID = "F28"
FEATURES = ["pax.newline-in-value.comment"]


def build(a):
    a.pax([(b"comment", b"x\n12 size=512")], note="a comment with a newline")
    a.header(b"a", b"0", 0, note="size 0")
    a.file(b"smuggled", b"", note="the data of a, to an implementation that splits records on lines")
    a.end()

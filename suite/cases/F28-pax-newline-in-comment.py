r"""A newline in a pax `comment`, which split on lines leaves a `size` record.

The archive has a file `a`, whose header has the size 0 and whose pax header has one record, a
`comment` with a newline in it, `x\n12 size=512`, then an empty file `smuggled`.

pax records are delimited by their length, so a comment can contain newlines, and in
[POSIX][comment] every comment is ignored: `a` has the size in its header, which is 0, and the next
block is the header of `smuggled`. This case is not ambiguous. A reader that splits records on
lines, and ignores their lengths, finds a second record, `size=512`, and takes the block for the
data of `a`, but POSIX has no such reading.

Seen in: none of the scanned tarballs. Newlines in pax values are only in xattrs, such as Minion
10.31, which the default policy accepts as xattrs are not extracted.
"""

F = lambda path, contents: {"path": path, "kind": "file", "contents": contents, "executable": False}

VERDICT = "accept"
ID = "F28"
TREE = [F("a", b""), F("smuggled", b"")]


def build(a):
    a.pax([(b"comment", b"x\n12 size=512")], note="a comment with a newline")
    a.header(b"a", b"0", 0, note="size 0")
    a.file(b"smuggled", b"", note="the data of a, to an implementation that splits records on lines")
    a.end()

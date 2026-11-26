r"""A newline in a pax `comment`, which split on lines leaves a `size` record.

The archive has a file `a` with size 0 in its ustar header and a single `comment` record containing
`x\n12 size=512` in its pax header, followed by an empty file `smuggled`.

Because pax records are delimited by their byte length, a comment may contain newlines, and
[POSIX][comment] requires ignoring every `comment` record. The file `a` therefore keeps its ustar
size of 0, and the next block is `smuggled`'s header. A reader that splits the pax payload on
newlines instead of using record lengths sees a spurious `size=512` record and consumes `smuggled`'s
header as `a`'s data.

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

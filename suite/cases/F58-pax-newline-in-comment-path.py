r"""A newline in a pax `comment`, which split on lines leaves a `path` record.

The archive has a file `a`, whose pax header has one record, a `comment` with a newline in it,
`x\n17 path=smuggled`.

pax records are delimited by their [length][record-length], so a comment can contain newlines, and
in [POSIX][comment] every comment is ignored: the file is `a`. This case is not ambiguous. A reader
that splits records on lines, and ignores their lengths, finds a second record, `path=smuggled`,
and extracts the file as `smuggled`.

Seen in: none of the scanned tarballs.
See also: F28, the same with a `size` record.
"""
F = lambda path, contents: {"path": path, "kind": "file", "contents": contents, "executable": False}

VERDICT = "accept"
ID = "F58"
FEATURES = ["pax.newline-in-value.comment"]
TREE = [F("a", b"a\n")]


def build(a):
    a.pax([(b"comment", b"x\n17 path=smuggled")], note="a comment with a newline")
    a.file(b"a", b"a\n")
    a.end()

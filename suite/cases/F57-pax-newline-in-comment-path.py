r"""A newline in a pax `comment`, which split on lines leaves a `path` record.

The archive has a file `a` whose pax header has a single `comment` record containing a newline:
`x\n17 path=smuggled`.

Because pax records are delimited by their [byte length][record-length], a comment may contain
newlines, and [POSIX][comment] requires ignoring every `comment` record, so the extracted file is
`a`. A reader that splits the pax payload on newlines instead sees a second record, `path=smuggled`,
and extracts the file as `smuggled`.

Seen in: none of the scanned tarballs.
See also: F28, the same with a `size` record.
"""
F = lambda path, contents: {"path": path, "kind": "file", "contents": contents, "executable": False}

VERDICT = "accept"
ID = "F57"
FEATURES = ["pax.newline-in-value.comment"]
TREE = [F("a", b"a\n")]


def build(a):
    a.pax([(b"comment", b"x\n17 path=smuggled")], note="a comment with a newline")
    a.file(b"a", b"a\n")
    a.end()

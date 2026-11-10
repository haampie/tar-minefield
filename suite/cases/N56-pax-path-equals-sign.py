"""A pax `path` that contains an equals sign, `a=b`.

The archive has one file, whose pax header has the record `path=a=b`, and whose header has the name
`header-name`.

After its length, a pax record is a keyword, followed by `=`, followed by a value, followed by a
newline, and a keyword [does not contain][keyword-equals] an equals sign. So the first `=` of the
record ends the keyword, the value is `a=b`, and the file has that name. A reader that splits the
record at its last `=` reads a keyword that it does not know, and extracts `header-name`.

Seen in: not measured, as the scans do not record the names of members.
"""
F = lambda path, contents: {"path": path, "kind": "file", "contents": contents, "executable": False}

VERDICT = "accept"
ID = "N56"
FEATURES = []
TREE = [F("a=b", b"which name?\n")]


def build(a):
    a.pax([(b"path", b"a=b")], note="a path with an equals sign")
    a.file(b"header-name", b"which name?\n")
    a.end()

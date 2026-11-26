"""A pax `path` value containing an equals sign: `a=b`.

The archive has one file with `path=a=b` in its pax header and `header-name` in its ustar name
field.

In a pax record `<length> <key>=<value>`, followed by a newline, the keyword [cannot
contain][keyword-equals] an equals sign. The first `=` therefore separates the keyword from the
value, giving `path` the value `a=b`. A reader that splits on the last `=` instead sees an unknown
key `path=a` and falls back to `header-name`.

Seen in: not measured, as the scanner does not record member names.
"""
F = lambda path, contents: {"path": path, "kind": "file", "contents": contents, "executable": False}

VERDICT = "accept"
ID = "N56"
FEATURES = []
TREE = [F("a=b", b"which name?\n")]


def build(a):
    a.pax([(b"path", b"a=b")], note="path=a=b")
    a.file(b"header-name", b"which name?\n")
    a.end()

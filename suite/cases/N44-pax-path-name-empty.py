"""A member with an empty name field and a pax `path`.

The archive has a file whose pax header has `path=a`, and whose header has an empty name field.

The pax `path` [overrides][path] the name and prefix fields, so the empty name field is not used,
and the file is `a`.

Seen in: none of the scanned tarballs.
See also: N17, an empty name, and N22, an empty pax `path`.
"""
F = lambda path, contents: {"path": path, "kind": "file", "contents": contents, "executable": False}

VERDICT = "accept"
ID = "N44"
FEATURES = []
TREE = [F("a", b"a\n")]


def build(a):
    a.pax([(b"path", b"a")])
    a.file(b"", b"a\n", note="an empty name field")
    a.end()

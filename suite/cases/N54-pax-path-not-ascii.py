"""A pax `path` in UTF-8 that is not ASCII.

The archive has one file, whose pax header has the `path` `日本語/café.txt`, in UTF-8, and whose header
has the name `nihongo/cafe.txt`.

In [POSIX][utf-8], pax records are UTF-8, and a `path` [overrides][path] the name of the header: it
is how a name that is not ASCII is stored in a pax archive. So the file is `日本語/café.txt`. A reader
that decodes the record in another encoding, such as Latin-1, extracts a file under another name.

Seen in: 789 of the scanned tarballs have names that are not ASCII, in a pax `path` or in the name
field.
See also: N03, a long name in a pax `path`, and N18, a name that is not UTF-8.
"""
F = lambda path, contents: {"path": path, "kind": "file", "contents": contents, "executable": False}
D = lambda path: {"path": path, "kind": "directory"}

VERDICT = "accept"
ID = "N54"
FEATURES = ["name.non-ascii"]
TREE = [D("日本語"), F("日本語/café.txt", b"which name?\n")]


def build(a):
    a.pax([(b"path", "日本語/café.txt".encode())], note="a path in UTF-8 that is not ASCII")
    a.file(b"nihongo/cafe.txt", b"which name?\n")
    a.end()

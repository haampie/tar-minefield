"""A directory with a long name in a pax `path`, then a file.

The archive has a directory whose pax header has a `path` of 120 `d`s, followed by a slash, and
whose header has the first 100 bytes of that path, then a file `a`.

The pax `path` [overrides][path] the name field of the directory, and an [extended header][extended]
applies to the next file only: the tree is the directory and `a`.

Seen in: tarballs with long names from Python's `tarfile` and GNU tar in pax format.
See also: N03, a long name of a file in a pax `path`.
"""
F = lambda path, contents: {"path": path, "kind": "file", "contents": contents, "executable": False}
D = lambda path: {"path": path, "kind": "directory"}

VERDICT = "accept"
ID = "N43"
FEATURES = []
TREE = [D("d" * 120), F("a", b"a\n")]


def build(a):
    a.pax([(b"path", b"d" * 120 + b"/")])
    a.directory(b"d" * 100)
    a.file(b"a", b"a\n")
    a.end()

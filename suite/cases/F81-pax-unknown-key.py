"""A pax header with a key that readers do not know.

The archive has a file `a`, whose pax header has the record `TARMINEFIELD.unknown=1`.

In [POSIX][keyword-extension], a key is either specified or an implementation extension, such as the
`SCHILY.*` keys of star, the `LIBARCHIVE.*` keys of libarchive and the `GNU.*` keys of GNU tar. It
is not specified what a reader does with a key that it does not know. A reader does not know the
extensions of every writer, and one that rejects an unknown key rejects the archives of the writers
that use it, so every implementation must extract `a`.

Seen in: tarballs of bsdtar and star, with keys such as `LIBARCHIVE.creationtime` and `SCHILY.dev`.
"""
F = lambda path, contents: {"path": path, "kind": "file", "contents": contents, "executable": False}

VERDICT = "accept"
ID = "F81"
FEATURES = []
TREE = [F("a", b"a\n")]


def build(a):
    a.pax([(b"TARMINEFIELD.unknown", b"1")], note="a key that readers do not know")
    a.file(b"a", b"a\n")
    a.end()

"""A pax header with an unrecognized vendor key.

The archive has a file `a` whose pax header contains `TARMINEFIELD.unknown=1`.

Beyond standard keywords, [POSIX][keyword-extension] permits vendor-prefixed extension keys such as
star's `SCHILY.*`, libarchive's `LIBARCHIVE.*` and GNU tar's `GNU.*`. POSIX does not say how a
reader should handle an unfamiliar key, but no reader knows every archiver's extensions, and
rejecting unknown keys would break archives from any writer that emits them, so every
implementation must extract `a`.

Seen in: tarballs from bsdtar and star, with keys such as `LIBARCHIVE.creationtime` and
`SCHILY.dev`.
"""
F = lambda path, contents: {"path": path, "kind": "file", "contents": contents, "executable": False}

VERDICT = "accept"
ID = "F81"
FEATURES = []
TREE = [F("a", b"a\n")]


def build(a):
    a.pax([(b"TARMINEFIELD.unknown", b"1")], note="unrecognized vendor key")
    a.file(b"a", b"a\n")
    a.end()

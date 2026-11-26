"""A ustar prefix and name under a pax header that has no `path` record.

The archive has one file with `p` in its prefix field, `a` in its name field, and a pax header
containing only `mtime=1`.

Each pax record overrides only its [corresponding][corresponding] ustar field, while any remaining
attribute [falls back to the ustar header][header-fallback]. Because the pax header has no `path`
record, the pathname still comes from concatenating the ustar [prefix][prefix], `/`, and name:
`p/a`. A reader that ignores the ustar prefix whenever a pax header is present extracts `a` at the
top level instead.

Seen in: 32 of the scanned tarballs, such as clamav 1.5.4 and Audacity 4.0.0, have members with a
ustar prefix and a pax header without `path`.
See also: N04, a name split across prefix and name, and N03, a long name in a pax `path`.
"""
F = lambda path, contents: {"path": path, "kind": "file", "contents": contents, "executable": False}
D = lambda path: {"path": path, "kind": "directory"}

VERDICT = "accept"
ID = "N58"
FEATURES = []
TREE = [D("p"), F("p/a", b"a\n")]


def build(a):
    a.pax([(b"mtime", b"1")], note="mtime=1, no path")
    a.file(b"a", b"a\n", prefix=b"p")
    a.end()

"""A name split between the prefix and name fields, under a pax header without a `path`.

The archive has one file whose prefix field is `p` and whose name field is `a`. Its pax header has
one record, `mtime=1`.

A pax record overrides the [corresponding][corresponding] field of the header, and an attribute
without a record [comes from the header][header-fallback]. The pax header does not have a `path`, so
the name is that of the header: the [prefix][prefix], followed by `/`, followed by the name, which
is `p/a`. A reader that drops the prefix of a member that has a pax header extracts `a`.

Seen in: 32 of the scanned tarballs, such as clamav 1.5.4 and Audacity 4.0.0, have members with a
prefix, and pax headers that do not have a `path`.
See also: N04, a name split between the prefix and name fields, and N03, a long name in a pax
`path`.
"""
F = lambda path, contents: {"path": path, "kind": "file", "contents": contents, "executable": False}
D = lambda path: {"path": path, "kind": "directory"}

VERDICT = "accept"
ID = "N58"
FEATURES = []
TREE = [D("p"), F("p/a", b"a\n")]


def build(a):
    a.pax([(b"mtime", b"1")], note="without a path record")
    a.file(b"a", b"a\n", prefix=b"p")
    a.end()

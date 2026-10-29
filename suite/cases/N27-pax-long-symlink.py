"""A symlink with a long name and a long target, in a pax `path` and `linkpath` respectively.

The archive has a file whose pax `path` is 120 `t`s, then a symlink to it, whose pax header has a
`path` of 120 `l`s and a `linkpath` of 120 `t`s. Their headers have the names cut to 100 bytes, as
writers put there.

In [POSIX][corresponding], a pax record overrides the corresponding field of the header, so the
symlink is the 120 `l`s, and points to the file of 120 `t`s before it.

Seen in: gnome-software 49.3.
"""

F = lambda path, contents: {"path": path, "kind": "file", "contents": contents, "executable": False}
L = lambda path, target: {"path": path, "kind": "symlink", "target": target}

VERDICT = "accept"
ID = "N27"
FEATURES = []
TREE = [F("t" * 120, b"target\n"), L("l" * 120, "t" * 120)]


def build(a):
    a.pax([(b"path", b"t" * 120)])
    a.file(b"t" * 100, b"target\n")
    a.pax([(b"path", b"l" * 120), (b"linkpath", b"t" * 120)])
    a.symlink(b"l" * 100, b"t" * 100)
    a.end()

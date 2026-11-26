"""A symlink with a long name and a long target, in a pax `path` and `linkpath` respectively.

The archive has a file whose pax `path` is 120 `t`s, followed by a symlink whose pax header sets
`path` to 120 `l`s and `linkpath` to 120 `t`s. Their ustar fields hold the first 100 bytes of each
name.

In [POSIX][corresponding], pax records override the corresponding ustar fields, so the symlink is
named with 120 `l`s and points to the file of 120 `t`s.

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

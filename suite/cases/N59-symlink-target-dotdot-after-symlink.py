"""A symlink target with `..` after a symlink component: `s/../x`.

The archive has the directories `d/` and `d/sub/`, a file `d/x`, a symlink `s` to `d/sub`, and a
symlink `t` to `s/../x`.

A symlink's target is stored verbatim as a [string][symlink-string], so `t` must be created with the
target `s/../x`. When the OS follows `t`, it resolves `s` to `d/sub` before applying `..`, reaching
`d/x`. A reader that lexically collapses `s/..` before creating the symlink changes the target to
`x`, a path that does not exist. Both targets stay inside the destination directory.

Seen in: not measured, as the scanner does not record symlink targets.
See also: N35, a symlink whose target escapes the destination.
"""
F = lambda path, contents: {"path": path, "kind": "file", "contents": contents, "executable": False}
D = lambda path: {"path": path, "kind": "directory"}
L = lambda path, target: {"path": path, "kind": "symlink", "target": target}

VERDICT = "accept"
ID = "N59"
FEATURES = []
TREE = [D("d"), D("d/sub"), F("d/x", b"x\n"), L("s", "d/sub"), L("t", "s/../x")]


def build(a):
    a.directory(b"d/")
    a.directory(b"d/sub/")
    a.file(b"d/x", b"x\n")
    a.symlink(b"s", b"d/sub")
    a.symlink(b"t", b"s/../x", note="resolves through s to d/x")
    a.end()

"""A symlink whose target has `..` after a component that is a symlink.

The archive has the directories `d/` and `d/sub/`, a file `d/x`, a symlink `s` to `d/sub`, then a
symlink `t` to `s/../x`.

The target of a symlink is a [string][symlink-string], which is not resolved when the link is
created, so `t` is created with the target `s/../x`. When `t` is followed, `s` is resolved first,
and `..` is then the parent of `d/sub`: the link leads to `d/x`. A reader that normalizes the target
as text removes `s/..`, and creates a link to `x`, which is not in the archive. Either target stays
inside the destination.

Seen in: not measured, as the scans do not record the targets of symlinks.
See also: N35, a symlink whose target leads out of the destination.
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
    a.symlink(b"t", b"s/../x", note="a target that leads to d/x")
    a.end()

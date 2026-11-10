"""A directory without write permission, before the file in it.

The archive has a directory `d/` with the mode 555, then a file `d/f`.

This is what a writer makes of a directory that is read-only: the directory first, with its mode,
and then its contents. A reader that gives the directory its mode when it creates it cannot create
`d/f` in it, unless it runs as root. It is in the [rationale of POSIX][dir-permissions] that a
reader can create a directory with enough permissions to create files in it, and set its mode after
all files are extracted. The mode of a directory is not part of the tree, which is `d` and `d/f`.

Seen in: not measured, as the scans do not record modes.
See also: S01, a directory after its contents.
"""
F = lambda path, contents: {"path": path, "kind": "file", "contents": contents, "executable": False}
D = lambda path: {"path": path, "kind": "directory"}

VERDICT = "accept"
ID = "S25"
FEATURES = []
TREE = [D("d"), F("d/f", b"f\n")]


def build(a):
    a.directory(b"d/", mode=0o555, note="read-only")
    a.file(b"d/f", b"f\n")
    a.end()

"""A directory after its contents.

The archive has the file `d/a`, then the directory `d/`, so `d` already exists when `d/` is
extracted.

[POSIX][dir-exists] says that extracting a directory that already exists is not an error.

Seen in: over a thousand tarballs.
"""

F = lambda path, contents: {"path": path, "kind": "file", "contents": contents, "executable": False}
D = lambda path: {"path": path, "kind": "directory"}

VERDICT = "accept"
ID = "S01"
FEATURES = []
TREE = [D('d'), F('d/a', b'a\n')]


def build(a):
    a.file(b"d/a", b"a\n")
    a.directory(b"d/")
    a.end()

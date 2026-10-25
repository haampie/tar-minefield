"""A directory after its contents.

Seen in: hundreds of tarballs.
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

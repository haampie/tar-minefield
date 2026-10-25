"""The same directory twice, as `tar cf x.tar d d/sub` writes.

Seen in: over a hundred tarballs.
"""

D = lambda path: {"path": path, "kind": "directory"}

VERDICT = "accept"
ID = "S02"
FEATURES = []
TREE = [D('d'), D('d/sub')]


def build(a):
    a.directory(b"d/")
    a.directory(b"d/sub/")
    a.directory(b"d/sub/")
    a.end()

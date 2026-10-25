"""The same directory twice, as `tar cf x.tar d d/sub` writes.

The archive has the directory `d/`, then `d/sub/` twice. POSIX says that extracting a directory
that already exists is not an error.

Seen in: over a hundred tarballs.
"""

D = lambda path: {"path": path, "kind": "directory"}

VERDICT = "accept"
ID = "S02"
FEATURES = []
POSIX = "dir-exists"
TREE = [D('d'), D('d/sub')]


def build(a):
    a.directory(b"d/")
    a.directory(b"d/sub/")
    a.directory(b"d/sub/")
    a.end()

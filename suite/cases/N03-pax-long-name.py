"""A name over 100 bytes, in a pax `path`.

The pax path is the name; the header has a truncated one, as writers put there.

Seen in: tarballs with long names from Python's `tarfile` and GNU tar in pax format.
"""

F = lambda path, contents: {"path": path, "kind": "file", "contents": contents, "executable": False}
D = lambda path: {"path": path, "kind": "directory"}

VERDICT = "accept"
ID = "N03"
FEATURES = []
TREE = [D('dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd'), F('dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd/ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff', b'long\n')]


def build(a):
    a.pax([(b"path", b"dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd/ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff")])
    a.file(b"dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd/fffffffffffffffffffffffffffffffffffffff", b"long\n")
    a.end()

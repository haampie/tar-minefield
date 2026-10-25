"""A member named `./`, the root of the tree, as `tar cf x.tar .` writes first.

The first member is the directory `./`, then the file `a`. The directory `./` is the one the
archive is extracted into, and the default policy normalizes it to the root of the tree.

Seen in: guile 2.0.9 and others.
"""

F = lambda path, contents: {"path": path, "kind": "file", "contents": contents, "executable": False}

VERDICT = "tolerate"
ID = "N05"
FEATURES = ['name.dot']
TREE = [F('a', b'a\n')]


def build(a):
    a.directory(b"./")
    a.file(b"a", b"a\n")
    a.end()

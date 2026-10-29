"""The name `./a`, which is the path `a`.

The archive has one file, `./a`.

The command `tar cf x.tar .` writes names that start with `./`. On a filesystem, `./a` and `a` are
one path, but implementations that compare names as strings see two: an index of `a` does not find
`./a`. In the default policy, `./a` and `a` in one archive are a duplicate.

Decision point: whether `./a` is `a`.
Seen in: hdf5 1.10.11, numdiff 5.9.0 and others.
"""

VERDICT = "tolerate"
ID = "N06"
FEATURES = ["name.leading-dot-slash"]
TREE = [
    {"path": "a", "kind": "file", "contents": b"a\n", "executable": False},
]


def build(a):
    a.file(b"./a", b"a\n")
    a.end()

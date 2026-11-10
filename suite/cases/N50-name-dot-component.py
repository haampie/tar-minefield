"""A name with a `.` component, `c/./d`.

The archive has one file, `c/./d`.

The special filename [dot][dot] refers to the directory that it is in, so in [POSIX][resolution] the
file is `c/d`. This case is ambiguous only to a reader that compares names as strings, to which
`c/./d` and `c/d` are two names for one path. The default policy tolerates it. In the default
policy, `c/./d` and `c/d` in one archive are a duplicate.

Decision point: whether a name is normalized before it is compared with others.
Seen in: 10 of the scanned tarballs, such as besu 24.1.2 and xdaliclock 2.49.
See also: N06, the name `./a`, and N49, a name with two consecutive slashes.
"""
F = lambda path, contents: {"path": path, "kind": "file", "contents": contents, "executable": False}
D = lambda path: {"path": path, "kind": "directory"}

VERDICT = "tolerate"
ID = "N50"
FEATURES = ["name.dot-component"]
TREE = [D("c"), F("c/d", b"d\n")]


def build(a):
    a.file(b"c/./d", b"d\n")
    a.end()

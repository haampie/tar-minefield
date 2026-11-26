"""A name with an inner `.` component: `c/./d`.

The archive has one file, `c/./d`.

Because [dot][dot] refers to its enclosing directory, [POSIX][resolution] resolves `c/./d` to `c/d`.
A reader that compares member names as raw strings fails to notice that `c/./d` and `c/d` name the
same file. The default policy tolerates `c/./d`, and treats `c/./d` and `c/d` in the same archive as
duplicates.

Decision point: whether `.` components are normalized before comparing member names.
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

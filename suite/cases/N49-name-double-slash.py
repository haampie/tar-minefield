"""A name with two consecutive slashes, `a//b`.

The archive has one file, `a//b`.

In POSIX, files are created by [pathname resolution][resolution], and in a pathname [consecutive
slashes][slashes] are the same as one, so the file is `a/b`. This case is ambiguous to a reader that
compares names as strings, to which `a//b` and `a/b` are two names for one path, and to one that
takes what is between the two slashes for a component with an empty name, which it cannot create.
The default policy tolerates it. In the default policy, `a//b` and `a/b` in one archive are a
duplicate.

Decision point: whether a name is normalized before it is compared with others.
Seen in: 2 of the scanned tarballs: shapemapper 2.1.5, and a binary distribution of GHC 9.0.2.
See also: N06, the name `./a`, and N50, a name with a `.` component.
"""
F = lambda path, contents: {"path": path, "kind": "file", "contents": contents, "executable": False}
D = lambda path: {"path": path, "kind": "directory"}

VERDICT = "tolerate"
ID = "N49"
FEATURES = ["name.double-slash"]
TREE = [D("a"), F("a/b", b"b\n")]


def build(a):
    a.file(b"a//b", b"b\n")
    a.end()

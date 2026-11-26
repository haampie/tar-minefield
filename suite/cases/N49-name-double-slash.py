"""A name with two consecutive slashes: `a//b`.

The archive has one file, `a//b`.

POSIX creates extracted files by [pathname resolution][resolution], which treats [multiple
consecutive slashes][slashes] as a single slash, resolving `a//b` to `a/b`. A reader that splits
paths on every slash sees an empty path component between the slashes and fails to create it, while
one that compares member names as raw strings fails to recognize `a//b` and `a/b` as the same path.
The default policy tolerates `a//b`, and treats `a//b` and `a/b` in the same archive as duplicates.

Decision point: whether consecutive slashes in a member name are collapsed.
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

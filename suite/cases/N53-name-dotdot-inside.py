"""A name with `..` that does not lead out of the destination, `a/../b`.

The archive has a directory `a/`, then a file `a/../b`.

The special filename [dot-dot][dot-dot] refers to the parent of the directory that it is in, so in
[POSIX][resolution] the file is `b`, next to `a`. This case is ambiguous in practice because a
reader can take the name in one of four ways. A reader that resolves the name extracts `b`. One that
drops the `..` extracts `a/b`. One that skips a member whose name has `..` extracts the directory
alone, without an error. Other readers report an error.

Decision point: whether a name with `..` is rejected, rewritten, skipped, or followed.
Seen in: 4 PyPI sdists, such as spdk 26.9 (`spdk-26.9/../scripts/rpc.py`) and bt-test-interfaces
0.0.5 (`bt-test-interfaces-0.0.5/../.git/config`), whose names do not lead out of the destination
either.
See also: N16, a name with `..` that leads out of the destination.
"""

VERDICT = "reject"
ID = "N53"
FEATURES = ["name.dotdot"]


def build(a):
    a.directory(b"a/")
    a.file(b"a/../b", b"b\n", note="a name with .. that resolves to b")
    a.end()

"""A name with `..` that stays inside the destination: `a/../b`.

The archive has a directory `a/`, followed by a file `a/../b`.

Because [dot-dot][dot-dot] refers to the parent directory, [POSIX][resolution] resolves `a/../b` to
`b` alongside `a`. Readers handle `a/../b` in four ways: resolve the path and extract `b`, strip the
`..` component and extract `a/b`, skip the member and leave only `a/`, or reject any path containing
`..`.

Decision point: whether a member name containing `..` is rejected, stripped, skipped, or resolved.
Seen in: 4 PyPI sdists, such as spdk 26.9 (`spdk-26.9/../scripts/rpc.py`) and bt-test-interfaces
0.0.5 (`bt-test-interfaces-0.0.5/../.git/config`), whose paths also stay inside the destination.
See also: N16, a name with `..` that escapes the destination.
"""

VERDICT = "reject"
ID = "N53"
FEATURES = ["name.dotdot"]


def build(a):
    a.directory(b"a/")
    a.file(b"a/../b", b"b\n", note="resolves to b")
    a.end()

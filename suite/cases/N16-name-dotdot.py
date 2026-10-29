"""A name with `..`, which climbs out of the directory the archive is extracted to.

The archive has one file, `tar-minefield/../../tar-minefield-escaped`, whose name resolves to a path
outside the destination.

The case is rejected because the name, taken as it is, leads out of the destination, not because it
is ambiguous. In [POSIX][resolution], files are created by pathname resolution, which follows the
name out of the destination. The file is harmless: its name and contents say what happened.

Decision point: whether a name with `..` is rejected, rewritten, skipped, or followed.
Seen in: 4 PyPI sdists, such as spdk 26.9 (`spdk-26.9/../scripts/rpc.py`) and bt-test-interfaces
0.0.5, whose `bt-test-interfaces-0.0.5/../.git/config` lands next to the top directory.
"""

VERDICT = "reject"
ID = "N16"
FEATURES = ["name.dotdot"]


def build(a):
    a.file(
        b"tar-minefield/../../tar-minefield-escaped",
        b"If this file is outside the directory you extracted to, the extractor followed `..`.\n",
    )
    a.end()

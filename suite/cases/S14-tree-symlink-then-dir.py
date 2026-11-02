"""A symlink to a directory, then a directory of the same name.

The archive has a directory `target/`, then a symlink `a` to `target`, then a directory `a/`.

The name `a/` can be seen as a pathname that [resolves][symlink-followed] through the symlink, as
the name ends in a slash, to the directory `target`, which [already exists][dir-exists], so
extracting it changes nothing. It can also be seen as the name of a directory `a`, of the member's
[own type][file-type], which either replaces the symlink, or results in a failure, as it cannot be
created where the symlink is.

Decision point: whether a directory member follows a symlink in its place.
Seen in: none of the scanned tarballs.
See also: S10, a symlink, then a file of the same name.
"""

VERDICT = "reject"
ID = "S14"
FEATURES = ["tree.duplicate.symlink-dir"]


def build(a):
    a.directory(b"target/")
    a.symlink(b"a", b"target")
    a.directory(b"a/")
    a.end()

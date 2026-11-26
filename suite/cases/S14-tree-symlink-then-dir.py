"""A symlink to a directory, then a directory of the same name.

The archive has a directory `target/`, a symlink `a` to `target`, and a directory `a/`.

Because `a/` ends in a slash, pathname resolution [follows][symlink-followed] the symlink `a` to the
existing directory `target`, where extracting an [already existing directory][dir-exists] is a
no-op, leaving `a` as a symlink to `target`. On the other hand, [POSIX][file-type] also says each
member is extracted with its archived file type: a reader that checks `a` without following the
symlink either replaces the symlink with a directory `a/` or fails because the symlink already
occupies that path.

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

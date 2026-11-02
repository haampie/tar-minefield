"""A symlink to a directory, then a directory of the same name.

The archive has a directory `target/`, then a symlink `a` to `target`, then a directory `a/`.

When a directory to extract [already exists][dir-exists], POSIX keeps it, and `a`, resolved through
the symlink, is the directory `target`. But a member is also extracted as a file of its [own
type][file-type], and `a` is a symlink, not a directory. This case is ambiguous because the
directory `a/` replaces the symlink, is taken to exist already, through it, or is an error.

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

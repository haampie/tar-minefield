"""A symlink to an absolute path, created as it is.

The archive has one symlink, `link`, to `/tar-minefield-nonexistent`, an absolute path that does not
exist.

The default policy tolerates it, and rejects an archive that writes through a symlink.

Seen in: tachyon 0.99.5, notmuch 0.40 and others.
See also: S10 and S11, archives that write through a symlink.
"""

L = lambda path, target: {"path": path, "kind": "symlink", "target": target}

VERDICT = "tolerate"
ID = "N07"
FEATURES = ['symlink.absolute']
TREE = [L('link', '/tar-minefield-nonexistent')]


def build(a):
    a.symlink(b"link", b"/tar-minefield-nonexistent")
    a.end()

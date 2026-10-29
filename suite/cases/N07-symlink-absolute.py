"""A symlink to an absolute path, created as it is.

The archive has one symlink, `link`, to `/tar-minefield-nonexistent`, an absolute path that does not
exist.

The default policy tolerates it, and rejects an archive that writes through a symlink, as S10 and
S11 do.

Seen in: tachyon 0.99.5, notmuch 0.40 and others.
"""

L = lambda path, target: {"path": path, "kind": "symlink", "target": target}

VERDICT = "tolerate"
ID = "N07"
FEATURES = ['symlink.absolute']
TREE = [L('link', '/tar-minefield-nonexistent')]


def build(a):
    a.symlink(b"link", b"/tar-minefield-nonexistent")
    a.end()

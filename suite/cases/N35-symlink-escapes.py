"""A relative symlink whose target leads out of the destination.

The archive has one member, a symlink `link` to `../escaped`, and does not write through it.

The default policy tolerates it, and rejects an archive that writes through a symlink.

Decision point: whether a symlink that points out of the destination is created.
Seen in: proteomics-runtime 0.3.8 and snowpark-checkpoints 0.1.0rc1.
See also: N07, a symlink to an absolute path, and S10 and S11, archives that write through a
symlink.
"""

L = lambda path, target: {"path": path, "kind": "symlink", "target": target}

VERDICT = "tolerate"
ID = "N35"
FEATURES = ["symlink.escapes"]
TREE = [L("link", "../escaped")]


def build(a):
    a.symlink(b"link", b"../escaped")
    a.end()

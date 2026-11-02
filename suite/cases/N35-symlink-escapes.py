"""A relative symlink whose target leads out of the destination.

The archive has one member, a symlink `link` to `../escaped`, and does not write through it.

Decision point: whether a symlink that points out of the destination is created.
Seen in: proteomics-runtime 0.3.8 and snowpark-checkpoints 0.1.0rc1.
See also: N07, a symlink to an absolute path, and S11, a member written through a symlink.
"""

VERDICT = "reject"
ID = "N35"
FEATURES = ["symlink.escapes"]


def build(a):
    a.symlink(b"link", b"../escaped")
    a.end()

"""A relative symlink whose target leads out of the destination.

The archive has one member, a symlink `link` to `../escaped`. No member is written through it.

The target of a symlink is [only a string][symlink-string] until it is used, so the archive has one
reading: a symlink `link` that points out of the destination. A strict parser rejects it all the
same: the tree it extracts then points outside itself, and whatever follows the link later, which
the archive does not control, reaches a file that it did not extract. A symlink to an absolute path
points out of the destination too, but real archives have those often enough, 89 of the scanned
tarballs, that the default policy tolerates them; relative ones that lead out are in 2.

Decision point: whether a symlink that points out of the destination is created.
Seen in: proteomics-runtime 0.3.8 and snowpark-checkpoints 0.1.0rc1.
See also: N07, a symlink to an absolute path, and S11, a member written through a symlink.
"""

VERDICT = "reject"
ID = "N36"
FEATURES = ["symlink.escapes"]


def build(a):
    a.symlink(b"link", b"../escaped")
    a.end()

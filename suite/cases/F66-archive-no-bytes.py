"""A zero-byte file: an empty archive, or not an archive?

The archive is 0 bytes long.

A [POSIX][end] archive ends with two zero blocks, which an empty file lacks. A zero-byte file can
be left behind by a failed download. Some readers accept it as an archive with no members, while
others reject it. The default policy tolerates it, as both extract the same empty tree, and whether
a download is complete is known by other means, such as a published checksum.

Decision point: whether a zero-byte file is a valid empty archive.
Seen in: none of the scanned tarballs.
See also: F65, an empty archive of two zero blocks, and F04, an archive without an end-of-archive
marker.
"""

VERDICT = "tolerate"
ID = "F66"
FEATURES = ["archive.empty"]
TREE = []


def build(a):
    pass

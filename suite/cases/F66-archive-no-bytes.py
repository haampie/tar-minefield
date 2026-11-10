"""A file of 0 bytes: an archive without members, or not an archive?

The archive is a file of 0 bytes.

In [POSIX][end], an archive ends with two zero blocks, which this file does not have. A download
that failed, or a file that was truncated, leaves such a file. This case is ambiguous in practice
because a reader either takes the end of the file for the end of an archive without members, and
extracts nothing without an error, or reports that the file is not an archive.

Decision point: whether a file of 0 bytes is an archive.
Seen in: none of the scanned tarballs.
See also: F65, an archive without members that ends with two zero blocks, and F04, an archive
without an end-of-archive marker.
"""

VERDICT = "reject"
ID = "F66"
FEATURES = ["archive.empty"]


def build(a):
    pass

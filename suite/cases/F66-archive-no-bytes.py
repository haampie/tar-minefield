"""A file of 0 bytes: an archive without members, or not an archive?

The archive has 0 bytes.

In [POSIX][end], an archive ends with two zero blocks, which this file does not have. Such a file
can be what is left of a download that failed. This case is ambiguous in practice because a reader
either takes the end of the file for the end of an archive without members, without an error, or
does not take the file for an archive, which is an error.

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

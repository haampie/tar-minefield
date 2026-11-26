"""A trailing pax extended header with no member after it.

The archive has a file `a`, a pax header with `path=renamed`, and then the end-of-archive marker.

In [POSIX][extended], a pax extended header describes the file that follows it. Here the archive
ends instead, as if truncated right before its last member. A reader either discards the dangling
pax header and extracts `a`, or reports an error.

Decision point: whether a trailing extended header with no member is an error.
Seen in: none of the scanned tarballs.
See also: F64, an archive that ends inside a header.
"""

VERDICT = "reject"
ID = "F67"
FEATURES = ["extended.without-member"]


def build(a):
    a.file(b"a", b"a\n")
    a.pax([(b"path", b"renamed")], note="dangling pax header")
    a.end()

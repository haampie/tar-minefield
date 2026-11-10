"""An extended header without a member after it.

The archive has a file `a`, then a pax header with the record `path=renamed`, then the
end-of-archive marker.

In [POSIX][extended], an extended header has the records of the file that follows it, and here a
file does not follow. Either the archive lost its last member, or its writer wrote a header too
many. This case is ambiguous in practice because a reader either ignores the header, and extracts
`a` without an error, or reports an error.

Decision point: whether an extended header without a member is an error.
Seen in: none of the scanned tarballs.
See also: F64, an archive that ends inside a header.
"""

VERDICT = "reject"
ID = "F67"
FEATURES = ["extended.without-member"]


def build(a):
    a.file(b"a", b"a\n")
    a.pax([(b"path", b"renamed")], note="the records of a member that is not there")
    a.end()

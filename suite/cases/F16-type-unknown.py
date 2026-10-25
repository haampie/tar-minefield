"""An unknown typeflag with a size: data, or no data?

POSIX says an unknown typeflag is read as a regular file, so the member has 512 bytes of data. This
case is ambiguous in practice because the member is also left out, and the block after its header
then either skipped as its data, or read as the header of `smuggled`.

Decision point: whether an unknown typeflag has data.
Seen in: no source tarball.
"""

VERDICT = "reject"
ID = "F16"
FEATURES = ['type.unknown-Z']


def build(a):
    a.header(b"unknown", b"Z", 512, note="typeflag Z, size 512")
    a.file(b"smuggled", b"", note="the data of the unknown member, read as a header by some")
    a.end()

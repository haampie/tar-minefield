"""An unknown typeflag with a size: data, or no data?

POSIX says an unknown typeflag is read as a regular file, so the 512 bytes after the header are the
data of `unknown`. Those bytes also form a valid header, of an empty file `smuggled`. This case is
ambiguous in practice because a reader that skips the member has to decide whether it has data. If
it does, the 512 bytes are skipped with it; if not, they are the header of the next member, and
`smuggled` is extracted.

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

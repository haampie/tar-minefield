"""An unknown typeflag with a size: data, or no data?

The archive has a member `unknown` of typeflag `Z`, which is not defined anywhere, with the size
512. The 512 bytes after its header also form a valid header, of an empty file `smuggled`.

[POSIX][unknown-type] says an unknown typeflag is read as a regular file, so those 512 bytes are the
data of `unknown`. This case is ambiguous in practice because a reader that skips the member, rather
than extract it as a file, has to decide whether it has data. If it does, the 512 bytes are skipped
with it; if not, they are the header of the next member, and `smuggled` is extracted.

Decision point: whether an unknown typeflag has data.
Seen in: none of the scanned tarballs.
"""

VERDICT = "reject"
ID = "F16"
FEATURES = ['type.unknown-Z']


def build(a):
    a.header(b"unknown", b"Z", 512, note="typeflag Z, size 512")
    a.file(b"smuggled", b"", note="the data of the unknown member, read as a header by some")
    a.end()

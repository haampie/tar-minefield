"""An unknown typeflag with a size: data, or no data?

The archive has a member `unknown` with an undefined typeflag `Z` and size 512. The 512-byte block
after its header is a valid header for an empty file `smuggled`.

Under [POSIX][unknown-type], an unrecognized typeflag is extracted as a regular file, making the
next 512 bytes `unknown`'s data. A reader that instead skips unknown member types must decide
whether `Z` carries data: skipping 512 bytes of data extracts nothing, whereas assuming `Z` has no
data treats the next block as `smuggled`'s header.

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

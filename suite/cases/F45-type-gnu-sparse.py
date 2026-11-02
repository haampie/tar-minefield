"""An old GNU sparse file, typeflag `S`: the data as stored, or the file it expands to?

The archive has one member, `a`, of typeflag `S` in the GNU format, whose header has a sparse map of
one region, 2 bytes at offset 1024, and the real size 1026. Its data is those 2 bytes, `ab`.

POSIX reserves the typeflags `A` to `Z` for [custom implementations][custom-type], and a reader that
does not recognize one extracts the member [as a regular file][unknown-type]: `a`, of 2 bytes. GNU's
format makes `a` a file of 1026 bytes, zeros but for the last two. The sparse map is where a ustar
header has the end of its prefix, so a reader that takes the header for ustar also finds a name
other than `a`. This case is ambiguous because `a` is the data as stored, or the file it expands
to.

Decision point: whether a sparse member is expanded.
Seen in: none of the scanned tarballs.
See also: N37, a sparse file in GNU's pax format.
"""

from blocks import octal

VERDICT = "reject"
ID = "F45"
FEATURES = ["type.gnu-sparse"]


def build(a):
    # The GNU header from offset 345, in the prefix field of ustar: atime, ctime, offset,
    # longnames and a byte unused (41 bytes), 4 sparse entries of offset and size (96), the flag
    # of an extended sparse header (1), the real size (12), then 5 bytes to the end of the field
    sparse = octal(1024, 12) + octal(2, 12) + bytes(72)
    gnu = bytes(41) + sparse + b"\0" + octal(1026, 12) + bytes(5)
    a.header(b"a", b"S", 2, magic=b"ustar ", version=b" \0", prefix=gnu,
             note="a GNU sparse file: 2 bytes at offset 1024 of 1026")
    a.data(b"ab", note="the one region of data")
    a.end()

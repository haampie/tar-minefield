"""A GNU volume label, typeflag `V`: a file, or skipped?

The archive has a header of typeflag `V`, in the GNU format, with the name `label` and the size 0,
then a file `a`.

GNU's format has the label of an archive as its first header, of typeflag `V`, which is not a file.
In POSIX, the typeflags `A` to `Z` are reserved for [custom implementations][custom-type], and a
reader that does not recognize one extracts the member [as a regular file][unknown-type]. This case
is ambiguous because the tree is either `a` alone, if the label is skipped, or an empty file `label`
as well.

Decision point: whether a volume label is extracted.
Seen in: none of the scanned tarballs.
See also: F16, an unknown typeflag with a size.
"""

VERDICT = "reject"
ID = "F52"
FEATURES = ["type.unknown-V"]
GNU = dict(magic=b"ustar ", version=b" \0")


def build(a):
    a.header(b"label", b"V", 0, note="a volume label", **GNU)
    a.file(b"a", b"a\n", **GNU)
    a.end()

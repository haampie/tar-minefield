"""A regular file `a/` with a size: a directory without data, or a file with data?

The archive has a regular file, of typeflag `0`, with the name `a/` and size 512. Its data is a
block that is the header of an empty file `smuggled`. Then a file `b`.

In POSIX, a regular file is followed by [(size+511)/512][records-follow] blocks of data, so the
header of `smuggled` is data. A member is extracted as a file of its [own type][file-type], but a
name that ends in a slash [resolves only to a directory][trailing-slash], so this is an
[error][cannot-create]. A name that ends in a slash was the [old way][slash-convention] to archive a
directory. This case is ambiguous in practice because a file has data and a directory does not. A
reader that goes by the typeflag extracts a file `a` of 512 bytes, and `b`. A reader that takes `a/`
for a directory either skips its 512 bytes, and extracts a directory `a` and `b`, or does not read
data for it, and extracts `smuggled` as well.

Decision point: whether a regular file whose name ends in a slash has data.
Seen in: not measured: 7 of the scanned tarballs have a regular file whose name ends in a slash,
such as sendmail 8.18.2, and the scans do not record its size.
See also: K01, the same with the size 0.
"""

VERDICT = "reject"
ID = "F60"
FEATURES = ["name.trailing-slash-on-file"]


def build(a):
    a.header(b"a/", b"0", 512, note="typeflag of a file, name of a directory, size 512")
    a.file(b"smuggled", b"", note="the data of a/, or a header after a directory without data")
    a.file(b"b", b"b\n")
    a.end()

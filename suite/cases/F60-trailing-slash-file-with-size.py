"""A regular file `a/` with a size: a directory without data, or a file with data?

The archive has a regular file (typeflag `0`) named `a/` with size 512, whose data block is a valid
header for an empty file `smuggled`, followed by a file `b`.

In POSIX, a regular file is followed by [(size+511)/512][records-follow] data blocks, making
`smuggled`'s header the data of `a/`. A member is extracted with its [archived file
type][file-type], yet a pathname ending in a slash [resolves only to a directory][trailing-slash],
resulting in an [error][cannot-create]. Before ustar added a directory typeflag, a trailing slash
was the [historical convention][slash-convention] for directories. Because regular files carry data
and directories do not, readers split in three ways: a reader that follows the typeflag extracts a
512-byte regular file `a` and `b`; one that treats `a/` as a directory and skips its 512 bytes
extracts a directory `a` and `b`; and one that treats `a/` as a directory with no data blocks also
extracts `smuggled`.

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

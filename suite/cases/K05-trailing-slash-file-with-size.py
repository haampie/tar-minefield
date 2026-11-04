"""A regular file named `a/` with a size: a directory without data, or a file with data?

The archive has a member whose header has typeflag `0`, a regular file, the name `a/` and the size
512, then a block that is the header of an empty file `smuggled`, as the data of `a/`, then a file
`b`.

In POSIX, a regular file is followed by [(size+511)/512][records-follow] blocks of data, so the
header of `smuggled` is data. A member is extracted as a file of its [own type][file-type], but a
name that ends in a slash [resolves only to a directory][trailing-slash], so this is an
[error][cannot-create]. A name that ends in a slash was the old way to archive a directory, in the
[rationale][slash-convention] of POSIX. This case is ambiguous in practice. A reader that goes by
the typeflag extracts a file `a` of 512 bytes, and `b`. A reader that takes `a/` for a directory
either skips its 512 bytes, and extracts a directory `a` and `b`, or reads no data for it, and
extracts `smuggled` as well.

Decision point: whether a regular file named like a directory has data.
Seen in: not measured: 8 of the scanned tarballs have a regular file whose name ends in a slash,
such as sendmail 8.18.2, and the scans do not record its size.
See also: K01, the same with the size 0.
"""

VERDICT = "reject"
ID = "K05"
FEATURES = ["name.trailing-slash-on-file"]


def build(a):
    a.header(b"a/", b"0", 512, note="typeflag of a file, name of a directory, size 512")
    a.file(b"smuggled", b"", note="the data of a/, or a header after a directory without data")
    a.file(b"b", b"b\n")
    a.end()

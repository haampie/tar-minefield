"""A regular file whose name ends in a slash: a file, or a directory?

The archive has one member, whose header has typeflag `0`, a regular file, and size 0, but the name
`a/`.

In [POSIX][file-type], a member is extracted as a file of its own type, but a name that ends in a
slash [resolves only to a directory][trailing-slash], so this is an [error][cannot-create]. A name
that ends in a slash was the old way to archive a directory, as the [rationale][slash-convention] of
POSIX recalls, but POSIX does not specify it. This case is ambiguous in practice because the member
is either a directory `a`, by its trailing slash, or an empty file `a`, by its typeflag.

Decision point: whether the typeflag or the trailing slash decides the kind.
Seen in: archives in the old v7 format, such as sendmail 8.18.2, tcp_wrappers 7.6 and
unclutter 8.
"""

VERDICT = "reject"
ID = "K01"
FEATURES = ["name.trailing-slash-on-file"]


def build(a):
    a.header(b"a/", b"0", 0, note="typeflag of a file, name of a directory")
    a.end()

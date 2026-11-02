"""A regular file with an empty name and a prefix: `dir/`, or no name?

The archive has one member, whose header has typeflag `0`, a regular file, size 0, an empty name
field, and the prefix `dir`.

In [POSIX][prefix], the pathname is the prefix, followed by `/`, followed by the name, which here is
empty, so the pathname is `dir/`. A member is extracted as a file of its [own type][file-type], here
a regular file, but a name that ends in a slash [resolves only to a directory][trailing-slash], so
this is an [error][cannot-create]. A name that ends in a slash was the old way to archive a
directory, before the typeflag of a directory existed, as the [rationale][slash-convention] of POSIX
recalls, but it is not part of POSIX. This case is ambiguous in practice because a reader that
follows that convention extracts a directory `dir`, a reader that goes by the typeflag extracts an
empty file `dir`, and a reader that takes the empty name field for a member without a name, before
it applies the prefix, extracts nothing.

Decision point: whether a prefix makes a name of an empty name field, and whether the typeflag or
the trailing slash decides the kind.
Seen in: 7 tarballs have a regular file whose name ends in a slash, such as sendmail 8.18.2, all in
the name field; none has an empty name with a prefix.
See also: K01, a regular file whose name ends in a slash, and N17, an empty name.
"""

VERDICT = "reject"
ID = "K04"
FEATURES = ["name.trailing-slash-on-file"]


def build(a):
    a.header(b"", b"0", 0, prefix=b"dir", note="an empty name, and the prefix dir")
    a.end()

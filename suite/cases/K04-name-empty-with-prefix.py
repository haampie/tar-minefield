"""A regular file with an empty name and a prefix: `dir/`, or no name?

The archive has one regular file (typeflag `0`) with size 0, an empty name field, and `dir` in its
prefix field.

Under [POSIX][prefix], the pathname is formed by joining the prefix, `/`, and the name, yielding
`dir/`. A member is extracted with its [archived file type][file-type] (a regular file), yet a
pathname ending in a slash [resolves only to a directory][trailing-slash], resulting in an
[error][cannot-create]. Before ustar added a directory typeflag, a trailing slash was the
[historical convention][slash-convention] for directories. Depending on the reader, the member is
extracted as a directory `dir` (by its trailing slash), as an empty regular file `dir` (by its
typeflag), or skipped as nameless if the reader checks for an empty name field before applying the
prefix.

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

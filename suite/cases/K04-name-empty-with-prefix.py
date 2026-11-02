"""A regular file with an empty name and a prefix: `dir/`, or no name?

The archive has one member, whose header has typeflag `0`, a regular file, size 0, an empty name
field, and the prefix `dir`.

In [POSIX][prefix], the pathname is the prefix, followed by `/`, followed by the name, which here
is `dir/`, a name that [resolves only to a directory][trailing-slash]. But the member is a regular
file, and a reader that finds the name field empty can take the member for one without a name
before it looks at the prefix. This case is ambiguous because the member is a directory `dir`, by
its slash, an empty file `dir`, by its typeflag, or a member without a name.

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

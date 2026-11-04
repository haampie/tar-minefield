"""A prefix in a header with GNU's magic and the version `00`: part of the name, or not?

The archive has one file, whose header has GNU's magic, `ustar` and a space, the version `00`, the
name `a` and the prefix `p`.

The [magic][magic] field specifies the format that the archive was written in. In the ustar
format, whose magic is `ustar` and a NUL, and whose [version][version] is `00`, the pathname is the
[prefix][prefix], a slash and the name. GNU's format has the magic `ustar` and a space, the version
of a space and a NUL, and other fields where ustar has its prefix. This case is ambiguous because
the header has the magic of one format and the version of the other, so that the file is `p/a`, read
as ustar, or `a`, read as GNU's format or as a v7 header, which has no prefix.

Decision point: which magic and version make the prefix part of the name.
Seen in: none of the scanned tarballs.
See also: N04, a name split by the ustar prefix, and N11, a GNU header with times where ustar has
its prefix.
"""

VERDICT = "reject"
ID = "F47"
FEATURES = ["magic.other"]


def build(a):
    a.file(b"a", b"a\n", magic=b"ustar ", version=b"00", prefix=b"p",
           note="GNU's magic, the version of POSIX, and a prefix")
    a.end()

"""A regular file whose name ends in a slash: a file, or a directory?

The header has typeflag `0`, a regular file, and size 0, but the name is `a/`. v7 tar had no
typeflag for directories, and wrote them like this. This case is ambiguous because the member is
either a directory `a`, by the convention of v7, or an empty file `a`, by its typeflag.

Decision point: whether the typeflag or the trailing slash decides the kind.
Seen in: v7 archives only, such as sendmail 8.18.2, tcp_wrappers 7.6 and unclutter 8.
"""

VERDICT = "reject"
ID = "K01"
FEATURES = ["name.trailing-slash-on-file"]


def build(a):
    a.header(b"a/", b"0", 0, note="typeflag of a file, name of a directory")
    a.end()

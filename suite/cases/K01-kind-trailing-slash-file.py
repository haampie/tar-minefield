"""A regular file whose name ends in a slash: a file, or a directory?

The archive has one regular file (typeflag `0`) with size 0 and the name `a/`.

Under [POSIX][file-type], a member is extracted with its archived file type, yet a pathname ending
in a slash [resolves only to a directory][trailing-slash], resulting in an [error][cannot-create].
Before ustar added a directory typeflag, a trailing slash was the [historical
convention][slash-convention] for directories. A reader that follows the trailing slash extracts a
directory `a`, whereas one that follows the typeflag extracts an empty regular file `a`.

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

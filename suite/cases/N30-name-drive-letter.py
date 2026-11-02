"""A name that starts with a drive letter, `C:/drive-letter`.

The archive has one file, named `C:/drive-letter`.

To POSIX, the name is [resolved][resolution] like any other: `C:` is a directory, and
`drive-letter` a file in it. On Windows, `C:/` is the root of a drive, so the same name is absolute.
This case is ambiguous because the file is `drive-letter` in a directory `C:` under the
destination, or `drive-letter` at the root of drive `C:`, outside it.

Decision point: whether a drive letter makes a name absolute.
Seen in: none of the scanned tarballs.
See also: N12, an absolute name.
"""

VERDICT = "reject"
ID = "N30"
FEATURES = ["name.drive-letter"]


def build(a):
    a.file(b"C:/drive-letter", b"in C:, or at the root of drive C:?\n")
    a.end()

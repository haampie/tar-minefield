"""A name that starts with a drive letter, `C:/drive-letter`.

The archive has one file, named `C:/drive-letter`.

Under [POSIX][resolution], `C:` is a normal directory name and `drive-letter` is a file inside it.
On Windows, `C:/` names the root of drive C, making the path absolute. A reader may extract
`drive-letter` inside a relative directory `C:`, write to the root of drive `C:` outside the
destination, or strip `C:/` (just as it strips a leading `/`) and extract `drive-letter` directly in
the destination.

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

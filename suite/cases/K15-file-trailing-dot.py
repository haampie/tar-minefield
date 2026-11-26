"""A regular file named `a/.`: a file `a`, or a directory?

The archive has one regular file (typeflag `0`) named `a/.`.

Because [dot][dot] refers to its enclosing directory, `a/.` resolves only if `a` is a directory, yet
[POSIX][file-type] requires extracting the member as a regular file, resulting in an
[error][cannot-create]. A reader that strips the trailing `/.` before extraction creates a regular
file `a`. A reader that first creates parent directories makes `a` a directory and then fails or
skips the file, leaving an empty directory `a`. A reader that renames the final `.` component
extracts a regular file inside `a`, such as `a/_`, while other readers report an error.

Decision point: whether a trailing `/.` on a regular file's name is stripped before extraction.
Seen in: not measured, as earlier scanner versions grouped trailing `/.` with inner `.` components;
10 scanned tarballs have a `.` component.
See also: K01, a regular file whose name ends in a slash, and N50, a name with an inner `.`
component.
"""

VERDICT = "reject"
ID = "K15"
FEATURES = ["name.trailing-dot-on-file"]


def build(a):
    a.file(b"a/.", b"a file, or in a directory?\n", note="typeflag of a file, name of a directory")
    a.end()

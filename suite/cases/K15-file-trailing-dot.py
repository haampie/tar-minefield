"""A regular file whose name ends in `/.`: a file `a`, or a directory?

The archive has one regular file, of typeflag `0`, with the name `a/.`.

The special filename [dot][dot] refers to the directory that it is in, so `a/.` is `a`, and resolves
only if `a` is a directory. In [POSIX][file-type], a member is extracted as a file of its own type,
so this is an [error][cannot-create]. This case is ambiguous in practice because a reader can take
the member in one of four ways. A reader that normalizes the name extracts a file `a`. One that
first creates the parent directories of a member extracts an empty directory `a`. One that renames a
component that it cannot create extracts the file under another name in that directory, such as
`a/_`. Other readers report an error.

Decision point: whether a name that ends in `/.` is normalized.
Seen in: not measured, as earlier versions of the scanner did not tell such a name apart from others
with a `.` component: 10 of the scanned tarballs have a name with such a component.
See also: K01, a regular file whose name ends in a slash, and N50, a name with a `.` component.
"""

VERDICT = "reject"
ID = "K15"
FEATURES = ["name.trailing-dot-on-file"]


def build(a):
    a.file(b"a/.", b"a file, or in a directory?\n", note="typeflag of a file, name of a directory")
    a.end()

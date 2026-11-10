"""A file in a directory that is not a member, then a file with the name of that directory.

The archive has a file `a/f`, then a file `a`. It does not have a member for the directory `a`.

To extract `a/f`, a reader [creates the directory][intermediate] `a`. The second member is a file at
the path of that directory. In [POSIX][file-type], a member is extracted as a file of its own type,
and existing files [can be overwritten][overwritten], but it is not specified whether a directory
and its contents are removed for it. This case is ambiguous because a reader can take the second
member in one of three ways. A reader that replaces what is at the path removes the directory with
`a/f`, and extracts the file `a` alone. One that keeps what is there leaves `a/f`, and skips the
file `a` without an error. Other readers report an error.

Decision point: whether a file replaces a directory that has contents.
Seen in: not measured, as earlier versions of the scanner compared the names of members only, and
the directory is not a member.
See also: S08, a file, then a directory of the same name, and S12, a member under a file.
"""

VERDICT = "reject"
ID = "S20"
FEATURES = ["tree.duplicate.dir-file"]


def build(a):
    a.file(b"a/f", b"f\n", note="in a directory that is not a member")
    a.file(b"a", b"a\n", note="a file at the path of that directory")
    a.end()

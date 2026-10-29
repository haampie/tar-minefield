"""A member with an empty name.

The archive has one file whose name field is all NULs.

The name is an empty pathname, which [does not resolve][null-pathname], so it would create an
invalid filename. In [POSIX][invalid-name], it is then implementation-defined whether the member is
stored, and under what name, and pax may [ignore it][ignore-invalid] if it reports an error. This
case is ambiguous because the member is then skipped with an error, stored under another name, such
as that of the archive, or taken for the destination directory itself, which fails. A reader that
takes the header for the end of the archive reads it against POSIX: the header is not a zero block,
and only [two zero blocks][end] end an archive.

Decision point: what an empty name refers to.
Seen in: none of the scanned tarballs.
"""

VERDICT = "reject"
ID = "N17"
FEATURES = ['name.empty']


def build(a):
    a.file(b"", b"no name\n")
    a.end()

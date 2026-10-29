"""A member under a file.

The archive has a file `a`, then a file `a/b`, whose name refers to `a` as a directory.

In [POSIX][intermediate], the directory `a` that `a/b` needs is made as with `mkdir()`, which fails
as `a` exists, so `a` is kept, `a/b` is not created, and pax writes a ["diagnostic
message"][cannot-create]. This case is ambiguous in practice because a reader that replaces the file
`a` with a directory, which is what the archives below mean, extracts `a/b` as well.

Decision point: whether a member under a file replaces it.
Seen in: sendmail 8.18.2 and unclutter 8, where the file is a v7 directory named `a/`.
"""

VERDICT = "reject"
ID = "S12"
FEATURES = ['tree.under-file']


def build(a):
    a.file(b"a", b"a file\n")
    a.file(b"a/b", b"under a file\n")
    a.end()

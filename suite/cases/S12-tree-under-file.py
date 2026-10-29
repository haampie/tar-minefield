"""A member under a file.

The first member is a file `a`, the second a file `a/b` in it. In POSIX, the directory `a` that
`a/b` needs is made as with `mkdir()`, which fails as `a` exists, so `a` is kept, `a/b` is not
created, and pax reports it. This case is ambiguous in practice because a reader may also replace
the file `a` with a directory, which is what the archives below mean.

Decision point: whether a member under a file replaces it.
Seen in: sendmail 8.18.2 and unclutter 8, where the file is a v7 directory named `a/`.
"""

VERDICT = "reject"
ID = "S12"
FEATURES = ['tree.under-file']
POSIX = {"POSIX": "intermediate", "reports": "cannot-create"}


def build(a):
    a.file(b"a", b"a file\n")
    a.file(b"a/b", b"under a file\n")
    a.end()

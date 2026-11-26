"""A member under a file.

The archive has a file `a`, followed by a file `a/b` whose path treats `a` as a directory.

Under [POSIX][intermediate], creating the parent directory `a` for `a/b` (as with `mkdir()`) fails
because `a` already exists as a regular file, so `a` is kept, `a/b` is not created, and the
extractor writes a [diagnostic message][cannot-create]. A reader that instead unlinks the regular
file `a` and replaces it with a directory extracts `a/b`.

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

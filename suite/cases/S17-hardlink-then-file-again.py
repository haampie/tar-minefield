"""A file, a hardlink to it, then the file again: does the link keep the first contents?

The archive has a file `a` that contains `first`, then a hardlink `b` to `a`, then a file `a` that
contains `second`.

A [hardlink][hardlink] is a second name for a file archived before it, and an existing file [can be
overwritten][overwrite]. In POSIX, it is not specified whether a file is overwritten in place, with
the new contents written into it, or replaced, with a new file in its place. Overwritten in place,
`a` and `b` are still one file, so `b` contains `second`. Replaced, `b` keeps the old file, which
contains `first`. This case is ambiguous because `b` contains either `first` or `second`, and `a`
contains `second` either way.

Decision point: whether a file is overwritten in place or replaced.
Seen in: 87 of the scanned tarballs have the same file twice, but none of them has a hardlink.
See also: S07, the same file twice with different contents, and S15, a file, then a hardlink of
the same name.
"""

VERDICT = "reject"
ID = "S17"
FEATURES = ["tree.duplicate.file-file"]


def build(a):
    a.file(b"a", b"first\n")
    a.hardlink(b"b", b"a")
    a.file(b"a", b"second\n", note="a again, with other contents")
    a.end()

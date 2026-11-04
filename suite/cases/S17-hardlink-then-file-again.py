"""A file, a hardlink to it, then the file again: does the link keep the first contents?

The archive has a file `a` that contains `first`, then a hardlink `b` to `a`, then a file `a` that
contains `second`.

A [hardlink][hardlink] is a link to a file archived before it, and existing files [can be
overwritten][overwritten], only when the tests of `-p`, `-u` and `-o invalid=` allow it. The
normative text does not say whether a file is overwritten in place, and so through every link to
it, or replaced by a new file; its [application usage][overwrite], which is informative, says that
overwriting may fail on the permissions of the first file, which fits writing in place. This case
is ambiguous because `b` contains `first`, if `a` is replaced, or `second`, if it is overwritten in
place, and `a` contains `second` either way.

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

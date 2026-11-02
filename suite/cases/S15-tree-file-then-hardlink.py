"""A file, then a hardlink of the same name to another file.

The archive has the files `a` and `b`, then a hardlink `a` to `b`.

The hardlink `a` either replaces the file `a`, as existing files [can be overwritten][overwritten],
so that `a` becomes a link to `b`, or results in a failure, as a link [cannot be
created][link-exists] where a file already is, which is an [error][link-error], and `a` keeps its
own contents.

Decision point: whether a hardlink replaces an existing file of its name.
Seen in: 27 tarballs have a file, then a hardlink of the same name, such as xscreensaver 6.12 and
atari++ 1.85, but each links to itself; none links to another file.
See also: S04, a hardlink to itself, and S07, the same file twice.
"""

VERDICT = "reject"
ID = "S15"
FEATURES = ["tree.duplicate.file-hardlink"]


def build(a):
    a.file(b"a", b"a\n")
    a.file(b"b", b"b\n")
    a.hardlink(b"a", b"b", note="a hardlink onto the file a")
    a.end()

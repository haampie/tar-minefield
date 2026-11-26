"""A file, then a hardlink of the same name to another file.

The archive has the files `a` and `b`, followed by a hardlink `a` to `b`.

Because POSIX permits [overwriting existing files][overwritten], a reader that unlinks `a` before
creating the hardlink replaces `a` with a link to `b`. A reader that calls `link()` directly fails
because the destination path [already exists][link-exists], which is an [error][link-error] and
leaves `a` with its original contents.

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

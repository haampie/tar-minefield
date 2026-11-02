"""A file, then a hard link of the same name to another file.

The archive has the files `a` and `b`, then a hard link `a` to `b`.

In POSIX, a hard link that cannot be created is [an error][link-error], and existing files are
[overwritten][overwritten] unless the options forbid it, but POSIX does not say whether a link
replaces a file of its name. This case is ambiguous because `a` is replaced by a link to `b`, or
keeps its own contents, with an error for the link.

Decision point: whether a hard link replaces an existing file of its name.
Seen in: 27 tarballs have a file, then a hard link of the same name, such as xscreensaver 6.12 and
atari++ 1.85, but each links to itself; none links to another file.
See also: S04, a hard link to itself, and S07, the same file twice.
"""

VERDICT = "reject"
ID = "S15"
FEATURES = ["tree.duplicate.file-hardlink"]


def build(a):
    a.file(b"a", b"a\n")
    a.file(b"b", b"b\n")
    a.hardlink(b"a", b"b", note="a hard link onto the file a")
    a.end()

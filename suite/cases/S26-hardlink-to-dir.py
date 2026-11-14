"""A hardlink to a directory.

The archive has a directory `d` with a file `d/f`, then a hardlink `h` to `d`.

In [POSIX][hardlink], a hardlink is a link to a file of any type archived before it, including a
directory. On most systems, a directory [cannot be linked][link-dir], and a link that cannot be made
is an [error][link-error], or its data is [restored from the original file][restore]. This case is
ambiguous in practice because a reader can take the link in one of five ways. A reader that creates
a member of the same kind as its target extracts an empty directory `h`. One that copies the target
where it cannot link extracts a copy of the directory with its contents, so that the tree has `h/f`.
One that makes a regular file of a link that it cannot create extracts an empty file `h`. One that
skips a link that it cannot make extracts `d` and `d/f` alone, without an error. Other readers
report an error.

Decision point: what a hardlink to a directory does.
Seen in: none of the scanned tarballs.
See also: S06, a hardlink to a symlink, and S03, a hardlink to a member that is not in the archive.
"""

VERDICT = "reject"
ID = "S26"
FEATURES = ["hardlink.to-dir"]


def build(a):
    a.directory(b"d")
    a.file(b"d/f", b"f\n")
    a.hardlink(b"h", b"d", note="a hardlink to a directory")
    a.end()

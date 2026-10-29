"""A member written through a symlink, which points out of the destination.

The archive has a symlink `d` to `..`, then a file `d/tar-minefield-through-symlink`.

The case is rejected because the file, written through the link, lands in the parent of the
destination, not because it is ambiguous: POSIX, which creates files by [pathname
resolution][resolution], requires writing through the link. The file is harmless.

Decision point: whether a member may be written through a symlink.
Seen in: none of the scanned tarballs.
"""

VERDICT = "reject"
ID = "S11"
FEATURES = ['tree.through-symlink']


def build(a):
    a.symlink(b"d", b"..")
    a.file(b"d/tar-minefield-through-symlink", b"If this file is outside the directory you extracted to, the extractor followed the name.\n")
    a.end()

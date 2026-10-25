"""A member written through a symlink, which points out of the destination.

The first member is a symlink `d` to `..`, the second a file `d/tar-minefield-through-symlink`. The
case is rejected because the file, written through the link, lands in the parent of the destination,
not because it is ambiguous. The file is harmless.

Decision point: whether a member may be written through a symlink.
Seen in: no source tarball.
"""

VERDICT = "reject"
ID = "S11"
FEATURES = ['tree.through-symlink']


def build(a):
    a.symlink(b"d", b"..")
    a.file(b"d/tar-minefield-through-symlink", b"If this file is outside the directory you extracted to, the extractor followed the name.\n")
    a.end()

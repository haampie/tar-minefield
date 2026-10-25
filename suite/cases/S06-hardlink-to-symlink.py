"""A hardlink to a symlink: a link to the symlink, or to its target?

The member `s` is a symlink to `f`, and `h` a hardlink to `s`. In POSIX, the target of a hardlink is
a file of any type, so `h` is a link to the symlink itself, another symlink to `f`. This case is
ambiguous in practice because `h` is also linked to the file `f` itself, or left out.

Decision point: whether a hardlink follows a symlink.
Seen in: octa 8.4.
"""

VERDICT = "reject"
ID = "S06"
FEATURES = ['hardlink.to-symlink']


def build(a):
    a.file(b"f", b"f\n")
    a.symlink(b"s", b"f")
    a.hardlink(b"h", b"s")
    a.end()

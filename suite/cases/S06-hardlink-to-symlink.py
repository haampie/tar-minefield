"""A hardlink to a symlink: a link to the symlink, or to its target?

The archive has a file `f`, a symlink `s` to `f`, and a hardlink `h` to `s`.

In [POSIX][hardlink], the target of a hardlink is a file of any type, so `h` is a second name for
the symlink `s` itself. But whether `link()` follows a symlink is
[implementation-defined][link-follows]; `linkat()` takes a flag for it. This case is ambiguous
because `h` is either a hard link to the symlink `s`, and so itself a symlink to `f`, or, with the
symlink followed, a hard link to the file `f`.

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

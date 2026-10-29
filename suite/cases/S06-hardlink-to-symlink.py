"""A hardlink to a symlink: a link to the symlink, or to its target?

The member `s` is a symlink to `f`, and `h` a hardlink to `s`. In [POSIX][hardlink], the target of a
hardlink is a file of any type, so `h` is a hard link to the symlink itself, a second name of `s`.
An extractor that makes it with `link()` may get either tree, depending on the system, as POSIX
leaves it [implementation-defined][link-follows] whether `link()` follows a symlink; `linkat()`
takes a flag for it. Readers also link `h` to the file `f` itself, make `h`, or both `h` and `s`,
empty files, or leave `h` out.

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

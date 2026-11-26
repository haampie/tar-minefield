"""A hardlink to a symlink: a link to the symlink, or to its target?

The archive has a file `f`, a symlink `s` to `f`, and a hardlink `h` to `s`.

Under [POSIX][hardlink], a hardlink can target a previously archived file of any type, making `h` a
second name for the symlink `s`. However, whether `link()` follows a symlink is
[implementation-defined][link-follows] (and controlled by a flag in `linkat()`). Depending on the
reader and platform, `h` becomes either a hardlink to the symlink `s` (and thus itself a symlink to
`f`) or a hardlink to the target file `f`.

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

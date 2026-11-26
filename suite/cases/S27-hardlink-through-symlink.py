"""A hardlink whose target path traverses a symlink.

The archive has a directory `d/`, a file `d/f`, a symlink `s` to `d`, and a hardlink `h` to `s/f`.

Under [POSIX][hardlink], a hardlink refers to a previously archived file. Although no member is
named `s/f`, resolving `s/f` on the filesystem follows the symlink `s` to the extracted member
`d/f`. A reader that resolves hardlink targets on the filesystem links `h` to `d/f`. A reader that
looks up the target by member name does not find `s/f` and either [reports an error][link-error] or
skips the link.

Decision point: whether a hardlink target is resolved on the filesystem or matched against member
names.
Seen in: none of the scanned tarballs.
See also: S16, a hardlink to `./a`, and S11, a member extracted through a symlink.
"""

VERDICT = "reject"
ID = "S27"
FEATURES = ["hardlink.missing-target"]


def build(a):
    a.directory(b"d/")
    a.file(b"d/f", b"f\n")
    a.symlink(b"s", b"d")
    a.hardlink(b"h", b"s/f", note="resolves through symlink s to d/f")
    a.end()

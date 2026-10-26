"""A hardlink to a symlink: a link to the symlink, or to its target?

The member `s` is a symlink to `f`, and `h` a hardlink to `s`. In POSIX, the target of a hardlink is
a file of any type, so `h` is a link to the symlink itself, another symlink to `f`, as GNU tar,
bsdtar, BusyBox, .NET, R, Rust's tar, astral-tokio-tar and containerd make it. But POSIX also leaves
it [implementation-defined](https://pubs.opengroup.org/onlinepubs/9799919799/functions/link.html#:~:text=If%20path1%20names%20a%20symbolic%20link%2C%20it%20is%20implementation%2Ddefined)
whether `link()` follows a symlink, so an extractor that links `h` to `s` with `link()` makes either
tree, depending on the system; `linkat()` takes a flag for it. Other implementations make other
trees: Python's `tarfile` and tar-fs link `h` to the file `f` itself; Archive::Tar makes `h` an
empty file, and Commons Compress and PharData make both `h` and `s` empty files; node-tar, RubyGems
and live-bootstrap's untar with `--non-strict` leave `h` out.

Decision point: whether a hardlink follows a symlink.
Seen in: octa 8.4.
"""

VERDICT = "reject"
ID = "S06"
FEATURES = ['hardlink.to-symlink']
POSIX = "hardlink"


def build(a):
    a.file(b"f", b"f\n")
    a.symlink(b"s", b"f")
    a.hardlink(b"h", b"s")
    a.end()

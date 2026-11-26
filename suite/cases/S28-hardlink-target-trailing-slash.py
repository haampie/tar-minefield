"""A hardlink to `a/`, where `a` is a regular file.

The archive has a regular file `a`, followed by a hardlink `h` with linkname `a/`.

A pathname with a trailing slash [resolves only to a directory][trailing-slash]. Because `a` is a
regular file, `a/` does not resolve as a filesystem path, and an uncreatable hardlink is an
[error][link-error]. A reader that strips trailing slashes from hardlink targets links `h` to `a`,
whereas one that passes `a/` to the OS or matches it verbatim against member names either reports an
error or skips the link.

Decision point: whether a trailing slash on a hardlink target is stripped.
Seen in: not measured, as earlier scanner versions stripped trailing slashes from hardlink targets;
2 scanned tarballs may have such a target.
See also: S16, a hardlink to `./a`, which is tolerated, and K05, a hardlink whose own name ends in a
slash.
"""

VERDICT = "reject"
ID = "S28"
FEATURES = ["hardlink.target-trailing-slash"]


def build(a):
    a.file(b"a", b"a\n")
    a.hardlink(b"h", b"a/", note="target a/ for regular file a")
    a.end()

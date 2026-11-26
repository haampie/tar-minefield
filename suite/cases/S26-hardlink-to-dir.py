"""A hardlink to a directory.

The archive has a directory `d`, a file `d/f`, and a hardlink `h` to `d`.

In [POSIX][hardlink], a hardlink refers to a previously archived file of any type, including a
directory. However, `link()` on a directory [fails on most systems][link-dir], and when a hardlink
cannot be created, the extractor must either [report an error][link-error] or [restore the data from
the original file][restore]. Readers handle `h` in five ways: create an empty directory `h` matching
the target's kind, recursively copy `d` so that the tree also contains `h/f`, fall back to creating
an empty regular file `h`, skip the uncreatable hardlink and extract only `d` and `d/f`, or report
an error.

Decision point: how a reader handles a hardlink to a directory.
Seen in: none of the scanned tarballs.
See also: S06, a hardlink to a symlink, and S03, a hardlink to a missing target.
"""

VERDICT = "reject"
ID = "S26"
FEATURES = ["hardlink.to-dir"]


def build(a):
    a.directory(b"d")
    a.file(b"d/f", b"f\n")
    a.hardlink(b"h", b"d", note="hardlink to directory d")
    a.end()

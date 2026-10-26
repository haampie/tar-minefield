"""A hardlink to itself.

The first member is a file `a`, the second a hardlink `a` to `a`. In POSIX, extracting a hardlink
to the same directory entry is an error. Read leniently, this case is ambiguous because the link
replaces `a`, which then has nothing to link to, empties it, or leaves it as it is.

Decision point: what a link to itself does to the file.
Seen in: 27 tarballs, 18 of them NVIDIA's cuDNN binaries in Spack, and xscreensaver 6.12 and
atari++ 1.85.
"""

VERDICT = "reject"
ID = "S04"
FEATURES = ['hardlink.to-itself']
POSIX = "same-entry"


def build(a):
    a.file(b"a", b"a\n")
    a.hardlink(b"a", b"a")
    a.end()

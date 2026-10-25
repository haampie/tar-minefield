"""A hardlink to a member that comes later.

The member `h` is a hardlink to `f`, which comes after it. In POSIX, a hardlink names a file
previously archived. Read leniently, this case is ambiguous because `h` either has nothing to link
to yet, or is linked to `f` once the whole archive is read.

Decision point: whether a hardlink may name a later member.
Seen in: no source tarball.
"""

VERDICT = "reject"
ID = "S05"
FEATURES = ['hardlink.to-later-member']


def build(a):
    a.hardlink(b"h", b"f")
    a.file(b"f", b"f\n")
    a.end()

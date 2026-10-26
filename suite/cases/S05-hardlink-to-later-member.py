"""A hardlink to a member that comes later.

The member `h` is a hardlink to `f`, which comes after it. In POSIX, the target of a hardlink is a
file previously archived. Read leniently, this case is ambiguous because `h` either has nothing to
link to yet, or is linked to `f` once the whole archive is read.

Decision point: whether the target of a hardlink can be a later member.
Seen in: none of the scanned tarballs.
"""

VERDICT = "reject"
ID = "S05"
FEATURES = ['hardlink.to-later-member']
POSIX = "hardlink"


def build(a):
    a.hardlink(b"h", b"f")
    a.file(b"f", b"f\n")
    a.end()

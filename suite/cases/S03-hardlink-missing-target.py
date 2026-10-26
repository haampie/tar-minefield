"""A hardlink to a member that is not in the archive.

The member `h` is a hardlink to `missing`. In POSIX, the target of a hardlink is a file previously
archived, which `missing` is not. Read leniently, this case is ambiguous because the link is either
skipped, or made to a file of that name that already exists where the archive is extracted.

Decision point: what a hardlink to nothing does.
Seen in: none of the scanned tarballs.
"""

VERDICT = "reject"
ID = "S03"
FEATURES = ['hardlink.missing-target']
POSIX = "hardlink"


def build(a):
    a.hardlink(b"h", b"missing")
    a.end()

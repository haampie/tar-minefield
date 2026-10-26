"""A hardlink with an empty target.

The first member is a file `a`, the second a hardlink `link` whose linkname field is empty. In
POSIX, the target of a hardlink is a file previously archived, and the archive contains no member
with the empty name, so as in S03 the link has nothing to link to. This case is ambiguous because
the link is skipped, or made to the destination directory itself, which fails, or made an empty
regular file `link`. It is a case of its own because implementations that refuse a hardlink to a
missing name may still take an empty one for no link at all.

Decision point: what a hardlink to the empty name does.
Seen in: none of the scanned tarballs.
See also: S03, a hardlink to a name that is not in the archive.
"""

VERDICT = "reject"
ID = "S13"
FEATURES = ["hardlink.missing-target"]
POSIX = "hardlink"


def build(a):
    a.file(b"a", b"a\n")
    a.hardlink(b"link", b"", note="a hardlink whose target is empty")
    a.end()

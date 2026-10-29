"""A hardlink with an empty target.

The archive has a file `a`, then a hardlink `link` whose linkname field is empty.

In [POSIX][hardlink], the target of a hardlink is a file previously archived, and the archive
contains no member with the empty name, so the link has nothing to link to. Read leniently, the link
is skipped instead. It is a case of its own because a reader that refuses a hardlink to a missing
name can still take an empty one for no link at all.

Decision point: what a hardlink to the empty name does.
Seen in: none of the scanned tarballs.
See also: S03, a hardlink to a name that is not in the archive.
"""

VERDICT = "reject"
ID = "S13"
FEATURES = ["hardlink.missing-target"]


def build(a):
    a.file(b"a", b"a\n")
    a.hardlink(b"link", b"", note="a hardlink whose target is empty")
    a.end()

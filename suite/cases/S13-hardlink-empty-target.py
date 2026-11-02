"""A hard link with an empty target.

The archive has a file `a`, then a hard link `link` whose linkname field is empty.

In [POSIX][hardlink], the target of a hard link is a file previously archived, which the archive
does not have, so the link has nothing to link to. Read leniently, the link is skipped instead.

Decision point: what a hard link to the empty name does.
Seen in: none of the scanned tarballs.
See also: S03, a hard link to a name that is not in the archive.
"""

VERDICT = "reject"
ID = "S13"
FEATURES = ["hardlink.missing-target"]


def build(a):
    a.file(b"a", b"a\n")
    a.hardlink(b"link", b"", note="a hardlink whose target is empty")
    a.end()

"""A hardlink to `/etc/passwd`, in an archive with a member `etc/passwd`.

The archive has a directory `etc`, a file `etc/passwd`, then a hardlink `l` to `/etc/passwd`.

A [hardlink][hardlink] is a link to a file archived before it, but here its target is an [absolute
pathname][absolute], which is not the name of any member. Some readers may normalize the target as
they normalize names, so that `/etc/passwd` is incorrectly taken for the member `etc/passwd`. This
case is ambiguous because `l` is either a link to that member, or to the file `/etc/passwd` outside
the destination.

Decision point: whether a hardlink may have an absolute target.
Seen in: not measured, as earlier versions of the scanner dropped the leading slash of the targets
of hardlinks: 28 of the scanned tarballs have a hardlink whose target may be absolute.
See also: N12, an absolute name, and S16, a hardlink to `./a`.
"""

VERDICT = "reject"
ID = "S18"
FEATURES = ["hardlink.absolute"]


def build(a):
    a.directory(b"etc")
    a.file(b"etc/passwd", b"the member etc/passwd\n")
    a.hardlink(b"l", b"/etc/passwd", note="a hardlink to an absolute path")
    a.end()

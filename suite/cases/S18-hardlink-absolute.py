"""A hardlink to an absolute path, which a member has as its name without the slash.

The archive has a directory `etc`, a file `etc/passwd`, then a hardlink `l` to `/etc/passwd`.

A [hardlink][hardlink] is a link to a file archived before it, and here its target is an [absolute
pathname][absolute], which is resolved from the root directory of the process and is the name of no
member. This case is ambiguous because `l` is a link to the member `etc/passwd`, if the leading
slash is dropped as it is from names, or to the file `/etc/passwd` outside the destination, linked
or copied, or is not created.

Decision point: whether the target of a hardlink is looked up in the archive or in the file system.
Seen in: not measured, as earlier versions of the scanner dropped the leading slash of the targets
of hardlinks: 28 of the scanned tarballs have a hardlink that may have one.
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

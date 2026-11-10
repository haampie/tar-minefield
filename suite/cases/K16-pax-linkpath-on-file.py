"""A regular file with a link target in its pax header.

The archive has one regular file, `a`, of typeflag `0`, whose pax header has the record
`linkpath=target`.

A `linkpath` record [overrides][linkpath] the linkname field, and in [POSIX][linkname] a linkname
has a meaning only for links. A member is extracted as a file of its [own type][file-type], so the
member is a file. This case is ambiguous only to a reader that goes by the link target, and makes a
link to `target`. Other readers extract the file, or report an error for a record that does not
belong to it.

Decision point: whether a link target makes a member a link.
Seen in: none of the scanned tarballs.
See also: K02, a regular file with a linkname.
"""

VERDICT = "reject"
ID = "K16"
FEATURES = ["extended.linkpath-on-file"]


def build(a):
    a.pax([(b"linkpath", b"target")], note="a link target for a file")
    a.file(b"a", b"a file, or a link?\n")
    a.end()

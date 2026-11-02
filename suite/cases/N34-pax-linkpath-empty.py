"""An empty pax `linkpath`, which in POSIX deletes a target: the pax one, or the header's too?

The archive has a symlink `link`, whose pax header has an empty `linkpath=`, and whose header has
the target `from-header`.

[POSIX][empty-value] says that a record with an empty value deletes any header block field of the
same name, and that pax ignores a field of the header that a keyword overrides or deletes, its
[corresponding][corresponding] field. No field of the header is named `linkpath`, which overrides
`linkname`. This case is ambiguous because, if deletion goes by the name of the keyword, `linkpath=`
deletes nothing in the header, and the target is `from-header`; if it goes by the field that the
keyword overrides, it deletes the target too, and leaves a symlink without one; and if the empty
value is the target, as POSIX [assigns][x-assigned] the value of a record, the symlink points to an
empty path.

Decision point: what an empty pax link path means: no target, an empty target, or the header's.
Seen in: none of the scanned tarballs.
See also: N22, an empty pax `path`, and N25, a symlink with an empty target.
"""

VERDICT = "reject"
ID = "N34"
FEATURES = ["pax.empty-value.linkpath"]


def build(a):
    a.pax([(b"linkpath", b"")], note="linkpath=, which removes the target")
    a.symlink(b"link", b"from-header")
    a.end()

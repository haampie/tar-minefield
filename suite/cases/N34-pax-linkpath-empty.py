"""An empty pax `linkpath`, which in POSIX deletes a target: the pax one, or the header's too?

The archive has a symlink `link`, whose pax header has an empty `linkpath=`, and whose header has
the target `from-header`.

In POSIX, a `linkpath` record [overrides][linkpath] the `linkname` field of the header, a record
with an empty value [deletes][empty-value] any field of the header of the same name, and a field of
the header that a keyword overrides or deletes [is ignored][corresponding]. The header does not have
a field named `linkpath`. So, if the empty value deletes by name, it deletes only the record, and
the target [comes from the header][header-fallback]: `from-header`. If it deletes the field that the
record overrides, `linkname` goes too, and the symlink is left without a target. If the record is
applied like any other, its empty value [becomes the target][x-assigned]. This case is ambiguous
because the target is `from-header`, missing, or empty.

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

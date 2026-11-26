"""An empty pax `linkpath`, which in POSIX deletes a target: the pax one, or the header's too?

The archive has a symlink `link` with an empty `linkpath=` record in its pax header and
`from-header` in its ustar linkname field.

In POSIX, `linkpath` [overrides][linkpath] the ustar `linkname` field, an empty value
[deletes][empty-value] any header field of the same name, and any header field overridden or deleted
by a pax record [is ignored][corresponding]. Because the ustar field is named `linkname` rather than
`linkpath`, `linkpath=` can be read in three ways: if it only clears a previous `linkpath`, the
target [falls back to the ustar header][header-fallback] (`from-header`); if it deletes the
overridden `linkname` field as well, the symlink is left without a target; and if the empty value is
[assigned directly][x-assigned], the symlink gets an empty target `""`.

Decision point: what an empty pax link path means: no target, an empty target, or the header's.
Seen in: none of the scanned tarballs.
See also: N22, an empty pax `path`, and N25, a symlink with an empty target.
"""

VERDICT = "reject"
ID = "N34"
FEATURES = ["pax.empty-value.linkpath"]


def build(a):
    a.pax([(b"linkpath", b"")], note="linkpath=, an empty target")
    a.symlink(b"link", b"from-header")
    a.end()

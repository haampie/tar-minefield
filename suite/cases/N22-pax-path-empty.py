"""An empty pax `path`, which in POSIX deletes a path: the pax one, or the header's name too?

The archive has one file with an empty `path=` record in its pax header and `from-header` in its
ustar name field.

Under [POSIX][empty-value], an empty pax value deletes any header field of the same name, and any
header field overridden or deleted by a pax record [is ignored][corresponding]. Because the ustar
header has `name` and `prefix` fields rather than a field literally named `path` (which
[overrides][path] both), `path=` can be read in two ways: if it only clears a previous `path`, the
member falls back to `from-header`; if it deletes the overridden ustar fields as well, the member is
left with an empty pathname, which [does not resolve][null-pathname].

Decision point: what an empty pax path means: no name, an empty name, or the header's name.
Seen in: none of the scanned tarballs.
"""

VERDICT = "reject"
ID = "N22"
FEATURES = ["pax.empty-value.path"]


def build(a):
    a.pax([(b"path", b"")], note="path=, which removes the path")
    a.file(b"from-header", b"which name?\n")
    a.end()

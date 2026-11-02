"""An empty pax `path`, which in POSIX deletes a path: the pax one, or the header's name too?

The archive has one file, whose pax header has an empty `path=`, and whose header has the name
`from-header`.

In [POSIX][empty-value], a record with an empty value deletes any header block field of the same
name, and a field of the header that a keyword deletes [is ignored][corresponding]. The header does
not have a field named `path`, which [overrides][path] `name` and `prefix`. This case is ambiguous
because, if deletion goes by the name of the keyword, `path=` deletes nothing in the header, and the
member is `from-header`; if it goes by the header field that the keyword overrides, it deletes the
name too, and leaves a member without a name, which is undefined, as an empty pathname [does not
resolve][null-pathname].

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

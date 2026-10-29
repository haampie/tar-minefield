"""An empty pax `path`, which in POSIX deletes a path: the pax one, or the header's name too?

The archive has one file, whose pax header has an empty `path=`, and whose header has the name
`from-header`.

[POSIX][empty-value] says that a record with an empty value deletes any header block field of the
same name, and that pax ignores a field of the header that a keyword deletes, its
[corresponding][corresponding] field. No field of the header is named `path`, which
[overrides][path] `name` and `prefix`. This case is ambiguous because, if deletion goes by the name
of the keyword, `path=` deletes nothing in the header, and the member is `from-header`; if it goes
by the header field that the keyword overrides, it deletes the name too, and leaves a member without
one, which POSIX does not define, as an empty pathname [does not resolve][null-pathname]. A reader
may also skip the member, or name the file after the archive.

An empty `linkpath` asks the same of a link: whether a symlink keeps the target in its header, has
an empty target, or is skipped. Implementations need not answer both alike: one that falls back to
the header's name for an empty `path` may still apply an empty `linkpath`.

Decision point: what an empty pax path means: no name, an empty name, or the header's name.
Seen in: none of the scanned tarballs.
See also: N25, a symlink with an empty target.
"""

VERDICT = "reject"
ID = "N22"
FEATURES = ["pax.empty-value.path"]


def build(a):
    a.pax([(b"path", b"")], note="path=, which removes the path")
    a.file(b"from-header", b"which name?\n")
    a.end()

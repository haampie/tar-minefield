"""An empty pax `path`, which in POSIX deletes a path: the pax one, or the header's name too?

POSIX says that a record with an empty value deletes any header block field of the same name, and
that pax ignores a field of the header that a keyword deletes, its corresponding field. No field of
the header is named `path`, which overrides `name` and `prefix`. This case is ambiguous because, if
deletion goes by the name of the keyword, `path=` deletes nothing in the header, and the member is
`from-header`; if it goes by the header field that the keyword overrides, it deletes the name too,
and leaves a member without one, which POSIX does not define, as an empty pathname [does not
resolve](https://pubs.opengroup.org/onlinepubs/9799919799/basedefs/V1_chap04.html#tag_04_16:~:text=A%20null%20pathname%20shall%20not%20be%20successfully%20resolved).
A reader may also skip the member, or name the file after the archive.

An empty `linkpath` asks the same of a link: whether a symlink keeps the target in its header, has
an empty target (see N25), or is skipped. Implementations need not answer both alike: one that falls
back to the header's name for an empty `path` may still apply an empty `linkpath`.

Decision point: what an empty pax path means: no name, an empty name, or the header's name.
Seen in: none of the scanned tarballs.
"""

VERDICT = "reject"
ID = "N22"
FEATURES = ["pax.empty-value.path"]
POSIX = {"POSIX": "empty-value", "overrides": "path", "corresponding": "corresponding"}


def build(a):
    a.pax([(b"path", b"")], note="path=, which removes the path")
    a.file(b"from-header", b"which name?\n")
    a.end()

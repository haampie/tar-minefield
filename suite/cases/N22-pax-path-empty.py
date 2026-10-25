"""An empty pax `path`, which in POSIX removes the path rather than giving one.

POSIX says that a record with an empty value deletes the corresponding field, in the header too, so
`path=` leaves the member with no name at all, not even that of its header, `from-header`. It does
not say what a member without a name is. This case is ambiguous because the name is either what the
header specifies, `from-header`, or empty (which refers to the destination itself).

Decision point: what an empty pax path means: no name, an empty name, or the header's name.
Seen in: no source tarball.
"""

VERDICT = "reject"
ID = "N22"
FEATURES = ["pax.empty-value.path"]
POSIX = "corresponding"


def build(a):
    a.pax([(b"path", b"")], note="path=, which removes the path")
    a.file(b"from-header", b"which name?\n")
    a.end()

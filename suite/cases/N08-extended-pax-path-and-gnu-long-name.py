"""A pax `path` and a GNU long name for one member, and a third name in its header.

The member has the name `from-header`, a GNU long name `from-gnu`, and a pax path `from-pax`.
Neither POSIX nor GNU's format defines the two extensions together. This case is ambiguous because
nothing says which of the three names wins: the member is `from-pax`, `from-gnu` or `from-header`.

Decision point: which of several sources gives a member its name.
Seen in: none of the scanned tarballs.
"""

VERDICT = "reject"
ID = "N08"
FEATURES = ['extended.pax-path-and-gnu-long-name']


def build(a):
    a.gnu_long(b"from-gnu")
    a.pax([(b"path", b"from-pax")])
    a.file(b"from-header", b"which name?\n")
    a.end()

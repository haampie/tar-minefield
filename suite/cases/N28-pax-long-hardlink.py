"""A hard link with a long name and a long target, in a pax `path` and `linkpath` respectively.

The archive has a file whose pax `path` is 120 `t`s, then a hard link to it, whose pax header has a
`path` of 120 `h`s and a `linkpath` of 120 `t`s. Their headers have the names cut to 100 bytes, as
writers put there.

In [POSIX][corresponding], a pax record overrides the corresponding field of the header, so the hard
link is the 120 `h`s, and links to the file of 120 `t`s before it.

Seen in: pyDACP 1.0.1.
"""

F = lambda path, contents: {"path": path, "kind": "file", "contents": contents, "executable": False}

VERDICT = "accept"
ID = "N28"
FEATURES = []
TREE = [F("t" * 120, b"target\n"), F("h" * 120, b"target\n")]


def build(a):
    a.pax([(b"path", b"t" * 120)])
    a.file(b"t" * 100, b"target\n")
    a.pax([(b"path", b"h" * 120), (b"linkpath", b"t" * 120)])
    a.hardlink(b"h" * 100, b"t" * 100)
    a.end()

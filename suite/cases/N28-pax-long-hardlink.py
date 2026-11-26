"""A hardlink with a long name and a long target, in a pax `path` and `linkpath` respectively.

The archive has a file whose pax `path` is 120 `t`s, followed by a hardlink whose pax header sets
`path` to 120 `h`s and `linkpath` to 120 `t`s. Their ustar fields hold the first 100 bytes of each
name.

In [POSIX][corresponding], pax records override the corresponding ustar fields, so the hardlink is
named with 120 `h`s and links to the file of 120 `t`s.

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

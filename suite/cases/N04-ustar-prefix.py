"""A long name split between the ustar prefix and name fields.

The prefix field is 120 `p`s and the name field is `file`. In [POSIX][prefix], the pathname is the
prefix, followed by `/`, followed by the name, so `file` is in a directory whose name is the 120
`p`s.

Seen in: thousands of tarballs.
"""

F = lambda path, contents: {"path": path, "kind": "file", "contents": contents, "executable": False}
D = lambda path: {"path": path, "kind": "directory"}

VERDICT = "accept"
ID = "N04"
FEATURES = []
TREE = [D('pppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppp'), F('pppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppp/file', b'prefixed\n')]


def build(a):
    a.file(b"file", b"prefixed\n", prefix=b"pppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppp")
    a.end()

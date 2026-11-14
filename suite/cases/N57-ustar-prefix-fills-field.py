"""A prefix of exactly 155 bytes, which fills the prefix field without a NUL.

The archive has one file whose prefix field is 155 `p`s, without a NUL, and whose name field is
`file`.

In [POSIX][prefix], the pathname is the prefix up to its first NUL, followed by `/`, followed by the
name. A prefix that fills its field does not have a NUL, and ends where the field ends, as a
[name][name-full] of 100 bytes does. So `file` is in a directory whose name is the 155 `p`s.

Seen in: not measured, as the scans do not record the length of a prefix: thousands of tarballs have
one.
See also: N02, a name that fills its field, and N04, a name split between the prefix and name
fields.
"""
F = lambda path, contents: {"path": path, "kind": "file", "contents": contents, "executable": False}
D = lambda path: {"path": path, "kind": "directory"}

VERDICT = "accept"
ID = "N57"
FEATURES = []
TREE = [D("p" * 155), F("p" * 155 + "/file", b"prefixed\n")]


def build(a):
    a.file(b"file", b"prefixed\n", prefix=b"p" * 155)
    a.end()

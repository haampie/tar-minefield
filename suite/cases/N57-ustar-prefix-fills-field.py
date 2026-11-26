"""A 155-byte ustar prefix that fills the entire field without a trailing NUL.

The archive has one file with 155 `p`s (and no NUL) in its prefix field and `file` in its name
field.

Under [POSIX][prefix], a member's pathname is its prefix (up to the first NUL), a slash, and its
name. Like a 100-byte name field, a full 155-byte prefix [does not need a terminating
NUL][name-full] and ends at the field boundary, placing `file` inside a directory of 155 `p`s.

Seen in: not measured, as the scanner does not record prefix lengths; thousands of tarballs use the
prefix field.
See also: N02, a 100-byte name without a NUL, and N04, a name split across prefix and name.
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

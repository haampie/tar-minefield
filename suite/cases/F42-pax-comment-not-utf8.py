r"""A pax `comment` that is not UTF-8.

The archive has one file, `a`, whose pax header has one record, a `comment` of the two bytes
`\xff\xfe`, which are not UTF-8.

In POSIX, the value of every specified keyword, `comment` among them, is in [UTF-8][utf-8-keyword],
and every [comment][comment] is ignored. The value can be seen as bound by the rule for UTF-8, which
makes the archive invalid, or as never read, as the comment is ignored. This case is ambiguous
because the archive is invalid, or has the file `a`.

Decision point: whether a comment is decoded before it is ignored.
Seen in: none of the scanned tarballs.
See also: F43, the same comment in a global header.
"""

F = lambda path, contents: {"path": path, "kind": "file", "contents": contents, "executable": False}

VERDICT = "tolerate"
ID = "F42"
FEATURES = ["pax.value-not-utf8.comment"]
TREE = [F("a", b"a\n")]


def build(a):
    a.pax([(b"comment", b"\xff\xfe")], note="a comment that is not UTF-8")
    a.file(b"a", b"a\n")
    a.end()

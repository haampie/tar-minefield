r"""A pax `comment` that is not UTF-8.

The archive has one file, `a`, whose pax header has a single `comment` record containing the two
non-UTF-8 bytes `\xff\xfe`.

In POSIX, every standard keyword value, including `comment`, is encoded in [UTF-8][utf-8-keyword],
yet every [comment][comment] is ignored. A reader that validates UTF-8 on all standard records
before ignoring comments rejects the archive, whereas one that skips `comment` records without
decoding them extracts `a`.

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

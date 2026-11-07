r"""A global pax `comment` that is not UTF-8.

The archive has a global header, typeflag `g`, with one record, a `comment` of the two bytes
`\xff\xfe`, which are not UTF-8, then a file `a`.

In POSIX, the value of every specified keyword, `comment` among them, is in [UTF-8][utf-8-keyword],
and every [comment][comment] is ignored. The value can be seen either as bound by the rule for
UTF-8, which makes the archive invalid, or as never read, as the comment is ignored. This case is
ambiguous because the archive is either invalid or has the file `a`.

Decision point: whether a comment is decoded before it is ignored.
Seen in: none of the scanned tarballs.
See also: F42, the same comment in an extended header.
"""

F = lambda path, contents: {"path": path, "kind": "file", "contents": contents, "executable": False}

VERDICT = "tolerate"
ID = "F43"
FEATURES = ["pax-global.value-not-utf8.comment"]
TREE = [F("a", b"a\n")]


def build(a):
    a.pax([(b"comment", b"\xff\xfe")], typeflag=b"g", name=b"pax_global_header",
          note="a comment that is not UTF-8")
    a.file(b"a", b"a\n")
    a.end()

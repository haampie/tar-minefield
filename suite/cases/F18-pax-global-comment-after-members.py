"""A global pax header with only a `comment`, after the first member.

The archive has the files `a` and `b`, and between them a global header, typeflag `g`, with the one
record `comment=after a`.

In [POSIX][comment], the value of a comment is ignored, so the header changes nothing for `b`.

Seen in: rpm 4.20.1 and x42-plugins 20230701.
"""

F = lambda path, contents: {"path": path, "kind": "file", "contents": contents, "executable": False}

VERDICT = "tolerate"
ID = "F18"
FEATURES = ['pax-global.after-members']
TREE = [F('a', b'a\n'), F('b', b'b\n')]


def build(a):
    a.file(b"a", b"a\n")
    a.pax([(b"comment", b"after a")], typeflag=b"g", name=b"pax_global_header")
    a.file(b"b", b"b\n")
    a.end()

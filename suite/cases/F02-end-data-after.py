"""Data after the end-of-archive marker that is not a header, which is ignored.

Seen in: tcp_wrappers 7.6, commons-lang 2.6 and xml-commons-resolver 1.2.
See also: F07, two concatenated archives, as `cat one.tar two.tar` makes them, which are rejected:
implementations either stop at the first two zero blocks or extract both archives.
"""

F = lambda path, contents: {"path": path, "kind": "file", "contents": contents, "executable": False}

VERDICT = "tolerate"
ID = "F02"
FEATURES = ['end.data-after']
TREE = [F('a', b'a\n')]


def build(a):
    a.file(b"a", b"a\n")
    a.end()
    a.raw(b"junk after the end of the archive\n", "junk: not a header")

"""Data after the end-of-archive marker that is not a header, which is ignored.

After the two zero blocks comes a block that starts with `junk after the end of the archive`. In
POSIX, the two zero blocks are the end of the archive, so the junk is not part of it, and the
default policy ignores it.

Seen in: tcp_wrappers 7.6, commons-lang 2.6 and xml-commons-resolver 1.2.
See also: F07, two concatenated archives, as `cat one.tar two.tar` makes them, which are rejected
because the second archive is either ignored or extracted as well.
"""

F = lambda path, contents: {"path": path, "kind": "file", "contents": contents, "executable": False}

VERDICT = "tolerate"
ID = "F02"
FEATURES = ['end.data-after']
POSIX = "end"
TREE = [F('a', b'a\n')]


def build(a):
    a.file(b"a", b"a\n")
    a.end()
    a.raw(b"junk after the end of the archive\n", "junk: not a header")

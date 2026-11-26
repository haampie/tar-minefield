"""A regular file with a link target.

The archive has one regular file, `a`, of typeflag `0`, with the linkname `target`.

[POSIX][linkname] gives a linkname meaning only for links, and a member is extracted as a file of
its [own type][file-type], so the member is a file. This case is ambiguous only to a reader that
goes by the linkname, and makes a link to `target`. The default policy tolerates it, as the readers
that accept it ignore the linkname and extract the same regular file.

Decision point: whether a linkname makes a member a link.
Seen in: bgen 1.1.7.
"""

F = lambda path, contents: {"path": path, "kind": "file", "contents": contents, "executable": False}

VERDICT = "tolerate"
ID = "K02"
FEATURES = ['linkname.on-file']
TREE = [F("a", b"a file, or a link?\n")]


def build(a):
    a.file(b"a", b"a file, or a link?\n", linkname=b"target")
    a.end()

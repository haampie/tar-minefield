"""A directory with a long name in a GNU long name, then a file.

The archive has a GNU long name header with a name of 120 `d`s, followed by a slash. After it is a
directory whose header has GNU's magic and the first 100 bytes of that name. Last is a file `a`,
also with GNU's magic.

The long name applies to the directory, and to no later member: the tree is the directory and `a`.
This is GNU tar's own format for long names.

Seen in: tarballs produced by GNU tar.
See also: N01, a long name of a file.
"""
F = lambda path, contents: {"path": path, "kind": "file", "contents": contents, "executable": False}
D = lambda path: {"path": path, "kind": "directory"}

VERDICT = "accept"
ID = "N42"
FEATURES = []
TREE = [D("d" * 120), F("a", b"a\n")]
GNU = dict(magic=b"ustar ", version=b" \0")


def build(a):
    a.gnu_long(b"d" * 120 + b"/")
    a.directory(b"d" * 100, **GNU)
    a.file(b"a", b"a\n", **GNU)
    a.end()

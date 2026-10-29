r"""The POSIX magic with NULs for its version, `ustar\0\0\0`, as some Java archivers write.

The magic of `a` is `ustar\0` and its version field is two NULs. In [POSIX][version], the version
field is `00`.

Seen in: commons-lang 2.6, apache-solr 3.6.2 and commons-logging 1.2.
"""

F = lambda path, contents: {"path": path, "kind": "file", "contents": contents, "executable": False}

VERDICT = "tolerate"
ID = "F05"
FEATURES = ['magic.posix-version-nuls']
TREE = [F('a', b'a\n')]


def build(a):
    a.file(b"a", b"a\n", version=b"\0\0")
    a.end()

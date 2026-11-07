"""A directory with an empty name field and a prefix.

The archive has one directory, of typeflag `5`, with an empty name field and the prefix `dir`.

In [POSIX][prefix], the pathname is the prefix, followed by `/`, followed by the name. The name is
empty here, so the pathname is `dir/`. The typeflag and the trailing slash both make the member a
directory `dir`.

Seen in: not measured, as the scans do not record an empty name field. Python's `tarfile` writes
one, with the prefix, for a directory whose last component is 100 bytes or longer, in a path of at
most 155 bytes, in the ustar format.
See also: K04, the same with a regular file.
"""
D = lambda path: {"path": path, "kind": "directory"}

VERDICT = "accept"
ID = "K07"
FEATURES = []
TREE = [D("dir")]


def build(a):
    a.header(b"", b"5", 0, prefix=b"dir", note="an empty name, and the prefix dir")
    a.end()

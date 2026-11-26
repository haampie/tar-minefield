"""A directory with an empty name field and a prefix.

The archive has one directory (typeflag `5`) with an empty name field and `dir` in its prefix field.

Under [POSIX][prefix], joining the prefix, `/`, and the empty name field yields `dir/`. Both the
typeflag and the trailing slash identify the member as the directory `dir`.

Seen in: not measured, as the scanner does not record an empty name field. In ustar mode, Python's
`tarfile` puts the path in the prefix field and leaves the name field empty for any directory whose
path is at most 155 bytes and whose final component is 100 bytes or longer.
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

"""The same directory twice, as `tar cf x.tar d d/sub` writes.

The archive has the directory `d/`, then `d/sub/` twice, then the file `d/sub/f`.
[POSIX][dir-exists] says that extracting a directory that already exists is not an error. The file
is there so that no directory is empty, which some implementations leave out. `tar cf x.tar d d/sub`
also writes the files in `d/sub` twice: bsdtar and BusyBox as two copies, which S09 rejects, and GNU
tar the second as a hard link to itself, which S04 rejects.

Seen in: over a hundred tarballs.
"""

D = lambda path: {"path": path, "kind": "directory"}
F = lambda path, contents: {"path": path, "kind": "file", "contents": contents, "executable": False}

VERDICT = "accept"
ID = "S02"
FEATURES = []
TREE = [D('d'), D('d/sub'), F('d/sub/f', b'f\n')]


def build(a):
    a.directory(b"d/")
    a.directory(b"d/sub/")
    a.directory(b"d/sub/")
    a.file(b"d/sub/f", b"f\n")
    a.end()

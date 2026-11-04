"""A NUL in the value of a pax xattr, before a `path` record.

The archive has a file whose pax header has the record `SCHILY.xattr.user.a`, whose value is `x`, a
NUL and `y`, then the record `path=renamed`, and whose header has the name `header-name`.

pax records are delimited by their [length][record-length], and [all characters][value-data] of a
value are data, so the NUL is part of the value of the xattr, and the file is `renamed`. This case
is not ambiguous. A reader that ends the data of a pax header at its first NUL loses the `path`
record after it, and extracts `header-name`, which is not a reading of POSIX.

Seen in: 32 of the scanned tarballs have a NUL in the value of an xattr, such as those of qd,
sundials and pacparser in Spack.
"""
F = lambda path, contents: {"path": path, "kind": "file", "contents": contents, "executable": False}

VERDICT = "accept"
ID = "F60"
FEATURES = ["pax.nul-in-value.SCHILY.xattr.*"]
TREE = [F("renamed", b"which name?\n")]


def build(a):
    a.pax([(b"SCHILY.xattr.user.a", b"x\0y"), (b"path", b"renamed")],
          note="an xattr with a NUL, then a path")
    a.file(b"header-name", b"which name?\n")
    a.end()

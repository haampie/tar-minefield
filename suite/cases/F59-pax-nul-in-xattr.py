"""A NUL in the value of a pax xattr, before a `path` record.

The archive has a file whose pax header has two records: `SCHILY.xattr.user.a`, whose value is
`x`, followed by a NUL, followed by `y`, and then `path=renamed`. Its header has the name
`header-name`.

pax records are delimited by their [length][record-length], and [all characters][value-data] of a
value are data, so the NUL is part of the value of the xattr, and the file is `renamed`. This case
is not ambiguous. A reader that ends the data of a pax header at its first NUL, or discards a header
that contains one, loses the `path` record, and extracts `header-name`.

Seen in: 32 of the scanned tarballs have a NUL in the value of an xattr, such as those of qd,
sundials and pacparser in Spack.
"""
F = lambda path, contents: {"path": path, "kind": "file", "contents": contents, "executable": False}

VERDICT = "accept"
ID = "F59"
FEATURES = ["pax.nul-in-value.SCHILY.xattr.*"]
TREE = [F("renamed", b"which name?\n")]


def build(a):
    a.pax([(b"SCHILY.xattr.user.a", b"x\0y"), (b"path", b"renamed")],
          note="an xattr with a NUL, then a path")
    a.file(b"header-name", b"which name?\n")
    a.end()

r"""An xattr in a pax header whose value is not UTF-8, as libarchive and star write them.

POSIX says that pax records are UTF-8, apart from names under `hdrcharset=BINARY`. But xattrs are
bytes, and libarchive and star write them in pax headers, as `LIBARCHIVE.xattr.*` (in base64) and
`SCHILY.xattr.*` (as they are). Here `SCHILY.xattr.user.data` is `\xff\xfe`. xattrs are not
part of the tree, and implementations that do not extract them can skip them without decoding
them, so every implementation must extract `a`.

Seen in: 31 source tarballs, such as R 4.5.2, Minion 10.31 and keepassxc 2.7.8, all in
`SCHILY.xattr.*`. No source tarball has another pax value that is not UTF-8, apart from names.
"""

VERDICT = "accept"
ID = "F31"
TREE = [
    {"path": "a", "kind": "file", "contents": b"a\n", "executable": False},
]


def build(a):
    a.pax([(b"SCHILY.xattr.user.data", b"\xff\xfe")], note="an xattr of two bytes that are not UTF-8")
    a.file(b"a", b"a\n")
    a.end()

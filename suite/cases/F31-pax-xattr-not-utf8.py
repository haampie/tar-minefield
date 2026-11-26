r"""An xattr in a pax header whose value is not UTF-8, as libarchive and star write them.

The archive has one file, `a`, whose pax header sets `SCHILY.xattr.user.data` to the two non-UTF-8
bytes `\xff\xfe`.

Under [POSIX][utf-8], pax records are encoded in UTF-8 except for path and name records under
`hdrcharset=BINARY`. However, extended attributes are arbitrary byte strings: star stores raw bytes
in `SCHILY.xattr.*`, and libarchive writes both `LIBARCHIVE.xattr.*` (in base64) and
`SCHILY.xattr.*` (raw bytes). Because extended attributes are not part of the extracted tree,
readers that ignore them can skip the record without UTF-8 decoding, and every implementation must
extract `a`.

Seen in: 31 release tarballs, such as R 4.5.2, Minion 10.31 and keepassxc 2.7.8, all in
`SCHILY.xattr.*`. No tarball scanned for it has another pax value that is not UTF-8, apart from
names.
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

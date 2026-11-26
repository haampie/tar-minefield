"""A name over 100 bytes, in a GNU long name.

The archive has a GNU long name header (typeflag `L`) whose payload is the next member's name—60
`d`s, a slash, and 60 `f`s—followed by a file with GNU magic whose ustar name field holds the first
100 bytes of that name.

Typeflag `L` is GNU tar's format for names that do not fit in the 100-byte ustar name field.

Seen in: tarballs produced by GNU tar.
"""

F = lambda path, contents: {"path": path, "kind": "file", "contents": contents, "executable": False}
D = lambda path: {"path": path, "kind": "directory"}

VERDICT = "accept"
ID = "N01"
FEATURES = []
TREE = [D('dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd'), F('dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd/ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff', b'long\n')]


def build(a):
    a.gnu_long(b"dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd/ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff")
    a.file(b"dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd/fffffffffffffffffffffffffffffffffffffff", b"long\n", magic=b"ustar ", version=b" \0")
    a.end()

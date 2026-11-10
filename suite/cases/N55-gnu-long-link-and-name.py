"""A symlink with a long name and a long target, in GNU's long link and long name headers.

The archive has a GNU long link name header, of typeflag `K`, whose data is 120 `t`s, followed by a
NUL. After it is a GNU long name header, of typeflag `L`, whose data is 120 `l`s, followed by a NUL.
After those is a symlink, of typeflag `2`, with GNU's magic, whose name and linkname fields contain
the first 100 bytes of each.

The long name replaces the name field, and the long link name the linkname field, so the symlink has
a name of 120 `l`s and points to 120 `t`s. GNU tar writes the two headers in this order.

Seen in: tarballs produced by GNU tar.
See also: N47, a long link name alone, and N01, a long name of a file.
"""
L = lambda path, target: {"path": path, "kind": "symlink", "target": target}

VERDICT = "accept"
ID = "N55"
FEATURES = ["linkname.no-nul"]
TREE = [L("l" * 120, "t" * 120)]
GNU = dict(magic=b"ustar ", version=b" \0")


def build(a):
    a.gnu_long(b"t" * 120, b"K")
    a.gnu_long(b"l" * 120)
    a.symlink(b"l" * 100, b"t" * 100, **GNU)
    a.end()

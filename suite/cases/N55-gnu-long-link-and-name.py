"""A symlink with both a GNU long link target (`K`) and a GNU long name (`L`).

The archive has a GNU long link header (typeflag `K`) containing 120 `t`s and a NUL, followed by a
GNU long name header (typeflag `L`) containing 120 `l`s and a NUL, and then a symlink (typeflag `2`)
with GNU magic whose ustar name and linkname fields hold the 100-byte prefixes.

The `L` header overrides the ustar name field and the `K` header overrides the linkname field,
producing a symlink named with 120 `l`s that points to 120 `t`s. GNU tar always emits `K` before `L`
when both are needed.

Seen in: tarballs produced by GNU tar.
See also: N47, a GNU long link name alone, and N01, a GNU long file name.
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

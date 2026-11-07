"""A symlink with a long target, in a GNU long link name.

The archive has a GNU long link name header, typeflag `K`, whose data is 120 `t`s, followed by a
NUL, then a symlink `l`, whose header has GNU's magic and, in its linkname field, the first 100
`t`s.

The long link name replaces the linkname field, so `l` points to the 120 `t`s. This is GNU tar's
own format for long link targets.

Seen in: tarballs produced by GNU tar.
See also: N01, a long name of a file, and N27, a long target in a pax `linkpath`.
"""
L = lambda path, target: {"path": path, "kind": "symlink", "target": target}

VERDICT = "accept"
ID = "N47"
FEATURES = ["linkname.no-nul"]
TREE = [L("l", "t" * 120)]
GNU = dict(magic=b"ustar ", version=b" \0")


def build(a):
    a.gnu_long(b"t" * 120, b"K")
    a.symlink(b"l", b"t" * 100, **GNU)
    a.end()

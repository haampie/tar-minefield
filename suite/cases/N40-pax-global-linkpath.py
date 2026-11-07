"""A global pax header with a `linkpath`.

The archive starts with a global header with `linkpath=global-target`, then has the symlinks `l` to
`header-target-l` and `m` to `header-target-m`.

In [POSIX][global], a global header applies to every later member, and a `linkpath`
[overrides][linkpath] the linkname field, so both symlinks point to `global-target`. This case is
ambiguous in practice because a reader that ignores the global `linkpath` keeps the targets of the
symlinks.

Decision point: whether a global `linkpath` applies.
Seen in: none of the scanned tarballs.
See also: N21, a global pax header with a `path`.
"""

VERDICT = "reject"
ID = "N40"
FEATURES = ["pax-global.linkpath"]


def build(a):
    a.pax([(b"linkpath", b"global-target")], typeflag=b"g", name=b"pax_global_header")
    a.symlink(b"l", b"header-target-l")
    a.symlink(b"m", b"header-target-m")
    a.end()

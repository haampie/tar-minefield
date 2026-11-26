"""A global pax header with a `linkpath`.

The archive starts with a global header containing `linkpath=global-target`, followed by symlinks
`l` (with ustar linkname `header-target-l`) and `m` (with ustar linkname `header-target-m`).

In [POSIX][global], a global header applies to every subsequent member that does not override it,
and `linkpath` [overrides][linkpath] the ustar linkname field, making both symlinks point to
`global-target`. A reader that ignores `linkpath` in a global header leaves `l` and `m` pointing to
their ustar targets.

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

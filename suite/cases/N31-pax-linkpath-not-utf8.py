r"""A pax `linkpath` that is not UTF-8.

The archive has a symlink `link` with `linkpath=caf\xe9` (`café` in Latin-1) in its pax header and
`from-header` in its ustar linkname field.

[POSIX][utf-8] says that pax records are UTF-8, apart from the values of `gname`, `linkpath`, `path`
and `uname` records under a `hdrcharset` record, [such as `hdrcharset=BINARY`][hdrcharset], which
this archive does not have. A link name that is not UTF-8 can be seen as one that [cannot be
translated][untranslatable], for which a diagnostic is required, and [by default][bypass] the file
is bypassed. Readers either use the raw bytes `caf\xe9`, decode or replace `\xe9` (yielding `café`
or `caf` followed by U+FFFD), discard the record they cannot decode and fall back to `from-header`,
or bypass the member or reject the archive.

Decision point: what a pax value that is not UTF-8 means.
Seen in: none of the scanned tarballs.
See also: N32, the same target in the header, and N24, a pax `path` that is not UTF-8, declared
as bytes with `hdrcharset=BINARY`.
"""

VERDICT = "reject"
ID = "N31"
FEATURES = ["pax.value-not-utf8.linkpath"]


def build(a):
    a.pax([(b"linkpath", b"caf\xe9")], note="a target that is not UTF-8")
    a.symlink(b"link", b"from-header")
    a.end()

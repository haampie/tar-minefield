r"""A pax `linkpath` that is not UTF-8.

The archive has a symlink `link` with `linkpath=caf\xe9` (`café` in Latin-1) in its pax header and
`from-header` in its ustar linkname field.

In [POSIX][utf-8], pax records use UTF-8 unless preceded by a `hdrcharset` record [such as
`hdrcharset=BINARY`][hdrcharset], which is absent here. An invalid UTF-8 value [cannot be
translated][untranslatable] to a UTF-8 locale, requiring a diagnostic and [by default][bypass]
bypassing the member. Readers either use the raw bytes `caf\xe9`, decode or replace `\xe9` (yielding
`café` or `caf` followed by U+FFFD), discard the invalid pax record and fall back to `from-header`,
or skip the member / reject the archive.

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

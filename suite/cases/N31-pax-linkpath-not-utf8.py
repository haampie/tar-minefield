r"""A pax `linkpath` that is not UTF-8.

The archive has a symlink `link`, whose pax header has `linkpath=caf\xe9`, `café` in Latin-1, and
whose header has the target `from-header`.

[POSIX][utf-8] says that pax records are UTF-8, apart from the values of `gname`, `linkpath`, `path`
and `uname` records under a `hdrcharset` record, [such as `hdrcharset=BINARY`][hdrcharset], which
this archive does not have. A link name that is not UTF-8 can be seen as one that [cannot be
translated][untranslatable], for which a diagnostic is required, and [by default][bypass] the file
is bypassed. This case is ambiguous because the target is the bytes as they are, `caf\xe9`; a
decoding of them, such as `café` or `caf` followed by U+FFFD; the header's `from-header`, to a
reader that drops a record it cannot decode; or there is no symlink at all, as the reader bypasses
the member, the default in POSIX, or rejects the archive as invalid.

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

r"""A pax path that is not UTF-8, declared as bytes with `hdrcharset=BINARY`.

The archive has one file with `hdrcharset=BINARY` and `path=caf\xe9` (`café` in Latin-1) in its pax
header, and `cafe` in its ustar name field.

With `hdrcharset=BINARY`, the pax path is [unencoded binary data][hdrcharset], here the raw bytes
`caf\xe9`. However, [POSIX][untranslatable] also requires a diagnostic message when a path cannot be
translated to the current locale's character set, and by default the file is [bypassed][bypass]. In
a UTF-8 locale, a reader may extract the raw bytes `caf\xe9`, decode or replace `\xe9`, fall back to
`cafe`, or bypass the file.

Decision point: whether a pax path declared as bytes is created as it is.
Seen in: none of the scanned tarballs.
"""

VERDICT = "reject"
ID = "N24"
FEATURES = ["pax.hdrcharset", "pax.path-not-utf8"]


def build(a):
    a.pax([(b"hdrcharset", b"BINARY"), (b"path", b"caf\xe9")], note="a path in Latin-1")
    a.file(b"cafe", b"which name?\n")
    a.end()

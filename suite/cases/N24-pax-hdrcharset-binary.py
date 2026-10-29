r"""A pax path that is not UTF-8, declared as bytes with `hdrcharset=BINARY`.

The archive has one file. Its pax header has `hdrcharset=BINARY` and the path `caf\xe9`, which is
`café` in Latin-1 and not UTF-8; its ustar header has the name `cafe`.

With `hdrcharset=BINARY`, the pax path is [unencoded binary data][hdrcharset], here the bytes
`caf\xe9`. But [POSIX][untranslatable] also requires pax to write a "diagnostic message" for a name
that cannot be translated "between the codeset in use for that extended header record and the
character set of the current locale", and by default [bypass][bypass] the file. This case is
ambiguous because the file is either created under those bytes, or bypassed, in a UTF-8 locale, to
which they cannot be translated.

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

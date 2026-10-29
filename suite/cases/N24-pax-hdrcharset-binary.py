r"""`hdrcharset=BINARY`, which declares a pax path that is not UTF-8 as bytes.

[POSIX][hdrcharset] lets a pax header declare with `hdrcharset=BINARY` that its names are bytes in
no particular encoding, rather than UTF-8, but also that a name that cannot be translated to the
character set of the locale is [reported][untranslatable], and by default bypassed. Here the path is
`caf\xe9`, in Latin-1. This case is ambiguous because the name on disk is those bytes, or, in a
UTF-8 locale, there is none, as the file is bypassed. In practice, the path is also decoded as
Latin-1, `café`, or with the byte replaced by U+FFFD, or discarded for the header's name, `cafe`. A
strict parser rejects names that are not UTF-8.

Decision point: how a name that is not UTF-8 becomes a path.
Seen in: none of the scanned tarballs.
"""

VERDICT = "reject"
ID = "N24"
FEATURES = ["pax.hdrcharset", "pax.path-not-utf8"]


def build(a):
    a.pax([(b"hdrcharset", b"BINARY"), (b"path", b"caf\xe9")], note="a path in Latin-1")
    a.file(b"cafe", b"which name?\n")
    a.end()

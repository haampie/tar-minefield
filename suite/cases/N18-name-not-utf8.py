r"""A name that is not UTF-8.

The name `caf\xe9` is Latin-1. [POSIX][ascii-header] requires the header to be in ISO/IEC 646, that
is ASCII, so the archive does not conform, and leaves the encoding of other characters in names to
the [implementation][name-encoding]. This case is ambiguous because the name on disk is those bytes,
or the name with the byte replaced, by U+FFFD or by `?`.

Decision point: how a name that is not UTF-8 is decoded.
Seen in: aspell-is 0.51.1-0 and aspell-nb 0.50.1-0.
"""

VERDICT = "reject"
ID = "N18"
FEATURES = ['name.not-utf8']


def build(a):
    a.file(b"caf\xe9", b"Latin-1\n")
    a.end()

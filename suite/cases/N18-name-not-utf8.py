r"""A name that is not UTF-8.

The name `caf\xe9` is Latin-1, and POSIX does not say how a name in the header is encoded. This case
is ambiguous because the name on disk is those bytes, `café` decoded as Latin-1, or the name with
the byte replaced.

Decision point: how a name that is not UTF-8 is decoded.
Seen in: aspell-is 0.51.1-0 and aspell-nb 0.50.1-0.
"""

VERDICT = "reject"
ID = "N18"
FEATURES = ['name.not-utf8']


def build(a):
    a.file(b"caf\xe9", b"Latin-1\n")
    a.end()

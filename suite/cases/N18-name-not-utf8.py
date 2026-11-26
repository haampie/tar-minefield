r"""A name that is not UTF-8.

The archive has one file, `caf\xe9`, with a Latin-1 name.

In [POSIX][ascii-header], ustar header characters come from ISO/IEC 646 (ASCII), and the encoding of
any other bytes in a filename is [implementation-defined][name-encoding]. Depending on the reader,
the extracted filename uses the raw bytes `caf\xe9`, or replaces `\xe9` with U+FFFD or `?`.

Decision point: how a name that is not UTF-8 is decoded.
Seen in: aspell-is 0.51.1-0 and aspell-nb 0.50.1-0.
"""

VERDICT = "reject"
ID = "N18"
FEATURES = ['name.not-utf8']


def build(a):
    a.file(b"caf\xe9", b"Latin-1\n")
    a.end()

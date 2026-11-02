r"""A global pax `comment` that is not UTF-8.

The archive has a global header, typeflag `g`, with one record, a `comment` of the two bytes
`\xff\xfe`, which are not UTF-8, then a file `a`.

POSIX says that the value of every keyword it [specifies][utf-8-keyword], `comment` among them, is
UTF-8, and that every [comment][comment] is ignored. So the archive is invalid, but a reader that
skips a comment never decodes it, and a reader that decodes every record before it looks at its
keyword finds the invalid one. This case is ambiguous because the archive is rejected, or has the
file `a`.

Decision point: whether a comment is decoded before it is ignored.
Seen in: none of the scanned tarballs.
See also: F42, the same comment in an extended header.
"""

VERDICT = "reject"
ID = "F43"
FEATURES = ["pax-global.value-not-utf8.comment"]


def build(a):
    a.pax([(b"comment", b"\xff\xfe")], typeflag=b"g", name=b"pax_global_header",
          note="a comment that is not UTF-8")
    a.file(b"a", b"a\n")
    a.end()

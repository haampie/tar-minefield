r"""A pax `comment` that is not UTF-8.

The archive has one file, `a`, whose pax header has one record, a `comment` of the two bytes
`\xff\xfe`, which are not UTF-8.

POSIX says that the value of every keyword it [specifies][utf-8-keyword], `comment` among them, is
UTF-8, and that every [comment][comment] is ignored. So the archive is invalid, but a reader that
skips comments might not validate the value, and a reader that decodes every record before it looks
at its keyword might realize it is invalid. This case is ambiguous because the archive is rejected,
or has the file `a`.

Decision point: whether a comment is decoded before it is ignored.
Seen in: none of the scanned tarballs.
See also: F43, the same comment in a global header.
"""

VERDICT = "reject"
ID = "F42"
FEATURES = ["pax.value-not-utf8.comment"]


def build(a):
    a.pax([(b"comment", b"\xff\xfe")], note="a comment that is not UTF-8")
    a.file(b"a", b"a\n")
    a.end()

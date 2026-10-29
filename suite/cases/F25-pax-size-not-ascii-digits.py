"""A pax `size` in Arabic-Indic digits, `٥١٢`, which some conversions of strings read as 512.

The archive has a file `a`, whose pax header has the size `٥١٢`, which is 512 in Arabic-Indic digits
(U+0665 U+0661 U+0662, in UTF-8), and whose header has the size 0, then an empty file `smuggled`.

In [POSIX][size-decimal], a pax size is ASCII decimal digits. Python's `int` and Java's
`Long.parseLong` take any decimal digit of Unicode, and so read it as 512. Read leniently, this case
is ambiguous because the size is either 512, as read that way (and the next block is the data of
`a`), or 0, as the header specifies (and the next block is the header of `smuggled`). Neither is a
reading of POSIX: `٥١٢` is not a pax size, and the header's size is to be [ignored][corresponding]
once a `size` record is there.

Decision point: which digits a pax number may have.
Seen in: none of the scanned tarballs.
"""

VERDICT = "reject"
ID = "F25"
FEATURES = ["pax.invalid-size"]


def build(a):
    a.pax([(b"size", "٥١٢".encode())], note="size=512 in Arabic-Indic digits, for a")
    a.header(b"a", b"0", 0, note="size 0")
    a.file(b"smuggled", b"", note="the data of a, to an implementation that reads 512")
    a.end()

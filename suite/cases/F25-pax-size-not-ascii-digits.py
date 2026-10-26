"""A pax `size` in Arabic-Indic digits, `٥١٢`, which some conversions of strings read as 512.

In POSIX, a pax size is ASCII decimal digits. Python's `int` and Java's `Long.parseLong` take any
decimal digit of Unicode, and so read `٥١٢` (U+0665 U+0661 U+0662, in UTF-8) as 512. Read
leniently, this case is ambiguous because the size is either that number, 512 (and the next block
is the data of `a`), or what the header specifies, 0 (and the next block is the header of
`smuggled`).

Decision point: which digits a pax number may have.
Seen in: none of the scanned tarballs.
"""

VERDICT = "reject"
ID = "F25"
FEATURES = ["pax.invalid-size"]
POSIX = "size-decimal"


def build(a):
    a.pax([(b"size", "٥١٢".encode())], note="size=512 in Arabic-Indic digits, for a")
    a.header(b"a", b"0", 0, note="size 0")
    a.file(b"smuggled", b"", note="the data of a, to an implementation that reads 512")
    a.end()

"""A pax `size` in Arabic-Indic digits, `٥١٢`, which some conversions of strings read as 512.

The archive has a file `a` whose pax header sets `size` to `٥١٢` (512 in UTF-8 Arabic-Indic digits,
U+0665 U+0661 U+0662) and whose ustar header has size 0, followed by an empty file `smuggled`.

In [POSIX][size-decimal], a pax size uses ASCII decimal digits. Read leniently, number parsers that
accept any Unicode decimal digit, such as Python's `int` and Java's `Long.parseLong`, parse `٥١٢` as
512 and consume the next block as `a`'s data, while a reader that rejects non-ASCII digits and falls
back to the ustar size of 0 reads the next block as `smuggled`'s header. Neither follows from POSIX,
which does not say what a `size` record that is not a decimal number means.

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

"""A GNU long name whose size leaves out its NUL, with bytes after it.

The archive has a GNU long name header of size 4, whose data block contains `name-rest`, followed by
NULs, so the size covers only `name`. Then a file whose header has GNU's magic and the name
`header-name`.

This case is ambiguous because the name ends either at the size, and is `name`, or at the first NUL
in the block, and is `name-rest`. This is not properly defined by GNU's format; all we know is that
archives created by GNU tar always include the NUL in the size. A lenient reader could also ignore a
long name without its NUL, and extract `header-name`. A reader that does not know typeflag `L` could
extract `header-name` too, after a file `@LongLink` that contains `name`.

Decision point: whether a GNU long name ends at its size or at a NUL.
Seen in: none of the scanned tarballs.
See also: N14, bytes after the NUL that ends a name.
"""

VERDICT = "reject"
ID = "N39"
FEATURES = ["gnu-long.no-nul"]
GNU = dict(magic=b"ustar ", version=b" \0")


def build(a):
    a.header(b"././@LongLink", b"L", 4, note="size 4: name, without its NUL", **GNU)
    a.raw(b"name-rest", "data: 4 bytes of name, then -rest")
    a.file(b"header-name", b"which name?\n", **GNU)
    a.end()

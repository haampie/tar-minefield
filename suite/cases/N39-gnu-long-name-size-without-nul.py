"""A GNU long name whose size leaves out its NUL, with bytes after it.

The archive has a GNU long name header (typeflag `L`) of size 4 whose data block contains
`name-rest` padded with NULs (so the 4-byte size covers only `name`), followed by a file with GNU
magic and `header-name` in its ustar name field.

GNU tar always includes the terminating NUL in the `L` header's size, and its format does not define
what happens when the size stops before the NUL. A reader that slices the payload to the declared
4-byte size extracts `name`, whereas one that reads the data block up to the first NUL extracts
`name-rest`. A reader that discards a long name lacking a NUL within its declared size falls back to
`header-name`, while one that does not recognize typeflag `L` extracts a 4-byte file `@LongLink`
followed by `header-name`.

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

"""A GNU long name whose size leaves out its NUL, with bytes after it.

The archive has a GNU long name header of size 4, whose data block has `name-rest` and NULs: the 4
bytes `name`, then `-rest`. Then a file whose header has GNU's magic and the name `header-name`.

GNU tar writes a long name with its NUL, which its size counts. This case is ambiguous because the
name ends at the size, and is `name`, or at the first NUL in the block, and is `name-rest`. A reader
that ignores a long name without its NUL gives `header-name`, and to a reader that does not know
typeflag `L`, the member is `header-name`, after a file `././@LongLink` that contains `name`.

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

"""An empty GNU long name: the name in the header, or none?

The archive has a GNU long name header (typeflag `L`) of size 0, followed by a file with GNU magic
and `header-name` in its ustar name field.

A GNU long name overrides the next member's ustar name field, and GNU's specification does not say
what a zero-length `L` header means. If it applies, the member's pathname is empty, and in POSIX an
[empty pathname][null-pathname] does not resolve. A reader that ignores the empty `L` header
extracts `header-name`. One that applies it gives the member an empty name, which is skipped,
rejected, or taken for `.`. One that uses the `L` header's own ustar name extracts `././@LongLink`,
while a reader that does not recognize typeflag `L` extracts an empty file `@LongLink` followed by
`header-name`.

Decision point: whether an empty GNU long name replaces the name in the header.
Seen in: none of the scanned tarballs.
See also: N17, an empty name, and N22, an empty pax `path`.
"""

VERDICT = "reject"
ID = "N38"
FEATURES = ["gnu-long.empty"]
GNU = dict(magic=b"ustar ", version=b" \0")


def build(a):
    a.header(b"././@LongLink", b"L", 0, note="an empty long name", **GNU)
    a.file(b"header-name", b"which name?\n", **GNU)
    a.end()

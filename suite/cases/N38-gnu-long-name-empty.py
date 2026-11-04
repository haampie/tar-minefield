"""An empty GNU long name: the name in the header, or none?

The archive has a GNU long name header of size 0, then a file whose header has GNU's magic and the
name `header-name`.

A GNU long name replaces the name of the next member, and GNU's format does not say what an empty
one means. If it applies, the pathname of the member is empty, and in POSIX an [empty
pathname][null-pathname] does not resolve. This case is ambiguous because the member is
`header-name`, if the empty long name is ignored; has an empty name, which is skipped, rejected or
taken for `.`; or is named after the long name header, `././@LongLink`. To a reader that does not
know typeflag `L`, the member is `header-name`, after an empty file `././@LongLink`.

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

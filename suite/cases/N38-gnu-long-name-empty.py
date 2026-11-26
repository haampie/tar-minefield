"""An empty GNU long name: the name in the header, or none?

The archive has a GNU long name header (typeflag `L`) of size 0, followed by a file with GNU magic
and `header-name` in its ustar name field.

A GNU long name overrides the next member's ustar name field, and GNU's specification does not say
what a zero-length `L` header means. A reader that ignores the empty `L` header extracts
`header-name`. A reader that applies the empty string gives the member an [empty
pathname][null-pathname], which is skipped, rejected, or resolved to `.`. A reader that accidentally
uses the `L` header's own ustar name extracts `././@LongLink`, while one that does not recognize
typeflag `L` extracts an empty file `@LongLink` followed by `header-name`.

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

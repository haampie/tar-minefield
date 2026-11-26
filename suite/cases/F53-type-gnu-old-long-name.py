"""A header of typeflag `N`, which some readers take for a long name: a name, or a file?

The archive has a GNU-format header of typeflag `N` named `././@LongLink` whose payload is
`long-name` followed by a NUL, and then a file with GNU magic and the ustar name `header-name`.

Some readers treat typeflag `N` as a GNU long name, like typeflag `L`. In POSIX, typeflags `A` to
`Z` are reserved for [custom implementations][custom-type], and a reader that does not recognize one
extracts it [as a regular file][unknown-type]. A reader that treats `N` as a long name extracts the
following member as `long-name`. A reader that extracts `N` as a regular file creates `@LongLink`
containing the name, followed by `header-name`, whereas one that skips unknown typeflags extracts
`header-name` alone.

Decision point: whether typeflag `N` is a long name.
Seen in: none of the scanned tarballs.
See also: F16, an unknown typeflag with a size, and N33, a Solaris extended header.
"""

VERDICT = "reject"
ID = "F53"
FEATURES = ["type.unknown-N"]
GNU = dict(magic=b"ustar ", version=b" \0")

NAME = b"long-name\0"


def build(a):
    a.header(b"././@LongLink", b"N", len(NAME), note="typeflag N", **GNU)
    a.raw(NAME, "data: a name and a NUL")
    a.file(b"header-name", b"which name?\n", **GNU)
    a.end()

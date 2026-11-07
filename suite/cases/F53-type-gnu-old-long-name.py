"""A header of typeflag `N`, which some readers take for a long name: a name, or a file?

The archive has a header of typeflag `N`, in the GNU format, with the name `././@LongLink`, whose
data is `long-name`, followed by a NUL, then a file whose header has GNU's magic and the name
`header-name`.

Some readers take typeflag `N` for a GNU long name, like typeflag `L`. In POSIX, the typeflags `A`
to `Z` are reserved for [custom implementations][custom-type], and a reader that does not recognize
one extracts the member [as a regular file][unknown-type]. This case is ambiguous because a reader
can take the `N` header in one of three ways. A reader that takes it for a long name extracts the
member as `long-name`. One that extracts it as a regular file extracts a file `@LongLink` that
contains the name, then `header-name`. One that skips a type it does not know extracts `header-name`
alone.

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

"""A header of typeflag `N`, which some readers take for a long name: a name, or a file?

The archive has a header of typeflag `N`, in the GNU format, with the name `././@LongLink`, whose
data is `long-name` and a NUL, then a file whose header has GNU's magic and the name `header-name`.

Some readers take typeflag `N` for a GNU long name, as `L`. In POSIX, the typeflags `A` to `Z` are
reserved for [custom implementations][custom-type], and a reader that does not recognize one
extracts the member [as a regular file][unknown-type]. This case is ambiguous because the member is
`long-name`, to a reader that takes `N` for a long name, or `header-name`, after a file
`././@LongLink` that contains the name, or alone, to a reader that skips a type it does not know.

Decision point: whether typeflag `N` is a long name.
Seen in: none of the scanned tarballs.
See also: F16, an unknown typeflag with a size, and N33, a Solaris extended header.
"""

VERDICT = "reject"
ID = "F54"
FEATURES = ["type.unknown-N"]
GNU = dict(magic=b"ustar ", version=b" \0")

NAME = b"long-name\0"


def build(a):
    a.header(b"././@LongLink", b"N", len(NAME), note="typeflag N", **GNU)
    a.raw(NAME, "data: a name and a NUL")
    a.file(b"header-name", b"which name?\n", **GNU)
    a.end()

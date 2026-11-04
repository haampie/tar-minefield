"""Two GNU long names for one member: the first, the last, or the header's?

The archive has two GNU long name headers, with `first` and `second`, then the member, whose header
has GNU's magic and the name `header-name`.

GNU's format does not say what two long names for one member mean. In POSIX, the typeflags `A` to
`Z` are reserved for [custom implementations][custom-type], and a reader that does not recognize one
extracts the member [as a regular file][unknown-type]. This case is ambiguous because the member is
`first` or `second`, to a reader that knows GNU long names, or `header-name`, to one that does not,
after two files `././@LongLink` that contain the names.

Decision point: which of two GNU long names applies.
Seen in: none of the scanned tarballs.
See also: N09, two pax extended headers for one member.
"""

VERDICT = "reject"
ID = "N37"
FEATURES = ["extended.two-gnu-long-names"]
GNU = dict(magic=b"ustar ", version=b" \0")


def build(a):
    a.gnu_long(b"first")
    a.gnu_long(b"second")
    a.file(b"header-name", b"which name?\n", **GNU)
    a.end()

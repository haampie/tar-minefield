"""A pax `path`, then a GNU long name, then the member: which name does it get?

The archive has a pax header with `path=from-pax`, a GNU long name header for `from-gnu`, and a file
whose ustar header gives the name `from-header`.

In POSIX, an [extended header][extended] applies to the file that follows it. Because typeflag `L`
is [reserved for custom implementations][custom-type], a pure POSIX reader extracts the `L` header
[as a regular file][unknown-type] named `from-pax` (containing `from-gnu\0`), followed by the file
`from-header`. Readers that support both extensions instead apply either `from-pax` or `from-gnu` to
the file member.

Decision point: which of several sources gives a member its name, and whether a pax header applies
to a GNU long name.
Seen in: none of the scanned tarballs.
See also: N08, a GNU long name, then a pax `path`, and F10, a pax `size`, then a GNU long name.
"""

VERDICT = "reject"
ID = "N29"
FEATURES = ["extended.pax-path-and-gnu-long-name"]


def build(a):
    a.pax([(b"path", b"from-pax")])
    a.gnu_long(b"from-gnu")
    a.file(b"from-header", b"which name?\n")
    a.end()

"""A pax `path`, then a GNU long name, then the member: which name does it get?

The archive has a pax header with `path=from-pax`, then a GNU long name `from-gnu`, then a file
whose header has the name `from-header`.

In POSIX, an [extended header][extended] applies to the file that follows it, which here is the GNU
long name: a typeflag `L`, which POSIX does not define, and so extracts [as a regular
file][unknown-type], with an error. Read by POSIX alone, the archive has a file `from-pax`, which
contains the long name, and the member `from-header`. Most readers that know GNU long names give the
member one of the two long names instead. This case is ambiguous for multiple reasons, because the
member is either `from-pax` or `from-gnu` for readers that support GNU long names; or a file
`from-pax` with the long name as contents followed by the file `from-header`.

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

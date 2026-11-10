"""A pax header whose own name leads out of the destination.

The archive has a pax header that is itself named `../tar-minefield-escaped`, with a `comment`
record, then a file `a`.

The name of an extended header is not the name of a member: a reader of pax reads its records, and
does not use its name. A reader of ustar from before the pax format [extracts the header as a
file][pre-pax-reader] of that name, which contains the records, and so does a reader that does not
recognize it as an extended header. Here that file is written outside the destination. This case is
ambiguous because the tree is either the file `a`, or `a` and a file next to the destination. That
file is harmless: its contents say what happened.

Decision point: whether the name of an extended header is checked as the name of a member is.
Seen in: not measured, as the scans record the names of extended headers without the components that
are those of a member: at most 1,003 of the scanned tarballs.
See also: N16, a member whose name has `..`, and F39, pax headers that a reader of v7 archives
extracts as files.
"""

VERDICT = "reject"
ID = "N52"
FEATURES = ["extended.name-dotdot"]


def build(a):
    a.pax([(b"comment", b"If this is a file outside the directory you extracted to, the extractor "
                        b"wrote a pax header as a file.")],
          name=b"../tar-minefield-escaped", note="named to lead out of the destination")
    a.file(b"a", b"a\n")
    a.end()

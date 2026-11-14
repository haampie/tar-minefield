"""A pax header whose own name leads out of the destination.

The archive has a pax header that is itself named `../tar-minefield-escaped`, with a `comment`
record, then a file `a`.

The name of an extended header is not the name of a member: a reader that knows pax reads its
records, and does not use its name. A reader of ustar before pax [extracts the header as a
file][pre-pax-reader] of that name, which contains the records, and a reader that does not recognize
the header does the same. In this archive, that file is written outside the destination. This case
is ambiguous because the tree is either the file `a`, or `a` and a file next to the destination.
That file is harmless: its contents say what happened.

Decision point: whether the name of an extended header is checked as the name of a member is.
Seen in: not measured, as the scans do not record the components of the name of an extended header
that come from its member: 1003 of the scanned tarballs may have such a name.
See also: N16, a name with `..`, and F39, pax headers after a v7 header.
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

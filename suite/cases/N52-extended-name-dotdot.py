"""A pax header whose own ustar name escapes the destination directory.

The archive has a pax header named `../tar-minefield-escaped` with a `comment` record, followed by a
file `a`.

A pax-aware reader parses an extended header's records and ignores its ustar name field, extracting
only `a`. However, a legacy ustar reader, or any reader that does not recognize typeflag `x`,
[extracts the pax header as a regular file][pre-pax-reader] containing the raw records. Here that
fallback writes `../tar-minefield-escaped` outside the destination directory (with a harmless text
payload explaining what happened).

Decision point: whether an extended header's ustar name is validated like a member name.
Seen in: not measured, as the scanner does not record the member-derived parts of an extended
header's name; 1003 scanned tarballs may have such a name.
See also: N16, a member name with `..`, and F39, pax headers after a v7 header.
"""

VERDICT = "reject"
ID = "N52"
FEATURES = ["extended.name-dotdot"]


def build(a):
    a.pax([(b"comment", b"If this is a file outside the directory you extracted to, the extractor "
                        b"wrote a pax header as a file.")],
          name=b"../tar-minefield-escaped", note="ustar name with ..")
    a.file(b"a", b"a\n")
    a.end()

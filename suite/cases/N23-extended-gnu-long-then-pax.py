"""A GNU long name, then a pax header, then the member: which of them does the long name apply to?

GNU long names and pax headers are two ways of extending the next header, and neither format defines
the other. Here a GNU long name `from-gnu` is followed by a pax header with only an `mtime`, and
then by the member `from-header`. This case is ambiguous because the long name applies either to the
next header, the pax header, and is lost, or to the next member, which is then `from-gnu` rather
than `from-header`.

Decision point: whether a GNU long name applies to the next header or to the next member.
Seen in: none of the scanned tarballs.
"""

VERDICT = "reject"
ID = "N23"
FEATURES = ["extended.gnu-long-and-pax"]


def build(a):
    a.gnu_long(b"from-gnu", note="the name of the next header, or of the next member")
    a.pax([(b"mtime", b"1")], note="only an mtime")
    a.file(b"from-header", b"which name?\n")
    a.end()

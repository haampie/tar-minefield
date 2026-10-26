"""A global `path`, then a global header that removes it with an empty value.

The first global header has `path=global-name`, which in POSIX applies to every later member. The
second has `path=`, which deletes it again, so the file after them keeps the name in its header,
`a`. This case is ambiguous in practice because a reader may instead take `path=` for an empty name,
or ignore it and keep `global-name`.

Decision point: whether an empty value in a global header removes an earlier global value.
Seen in: none of the scanned tarballs.
See also: N21, a global `path`, and N22, an empty `path` in an extended header.
"""

VERDICT = "reject"
ID = "N26"
FEATURES = ["pax-global.path", "pax-global.empty-value.path"]
POSIX = {"POSIX": "global", "deletes": "empty-value"}


def build(a):
    a.pax([(b"path", b"global-name")], typeflag=b"g", name=b"pax_global_header",
          note="path=global-name, for every later member")
    a.pax([(b"path", b"")], typeflag=b"g", name=b"pax_global_header",
          note="path=, which removes the global path")
    a.file(b"a", b"which name?\n")
    a.end()

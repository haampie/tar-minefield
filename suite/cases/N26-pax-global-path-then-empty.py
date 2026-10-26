"""A global `path`, then a global header that removes it with an empty value.

The first global header has `path=global-name`, which in POSIX names every later member, as in
N21. The second has `path=`, and an empty value in a global header deletes the earlier global value,
so `a` has its own name again. This case is ambiguous in practice because, with the deletion
ignored, `a` is named `global-name`; with the empty value read as an empty name, `a` has no name at
all; and with global headers ignored altogether, `a` keeps its own name for another reason.

Decision point: whether an empty value in a global header removes an earlier global value.
Seen in: none of the scanned tarballs.
See also: N21, a global `path`, and N22, an empty `path` in an extended header.
"""

VERDICT = "reject"
ID = "N26"
FEATURES = ["pax-global.path", "pax-global.empty-value.path"]
POSIX = "empty-value"


def build(a):
    a.pax([(b"path", b"global-name")], typeflag=b"g", name=b"pax_global_header",
          note="every later member is named global-name")
    a.pax([(b"path", b"")], typeflag=b"g", name=b"pax_global_header",
          note="path=, which removes the global path")
    a.file(b"a", b"which name?\n")
    a.end()

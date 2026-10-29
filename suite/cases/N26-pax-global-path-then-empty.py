"""A global `path`, then a global header that removes it with an empty value.

The first global header has `path=global-name`, which in [POSIX][global] applies to every later
member. The second has `path=`, which [deletes][empty-value] it again, so the file after them keeps
the name in its header, `a`. POSIX deletes the global value by name; whether the deletion also
reaches the name in the header is the question of N22, so the file may also be left without a name.
This case is ambiguous in practice because a reader may instead take `path=` for an empty name, or
ignore it and keep `global-name`.

Decision point: whether an empty value in a global header removes an earlier global value.
Seen in: none of the scanned tarballs.
See also: N21, a global `path`, and N22, an empty `path` in an extended header.
"""

VERDICT = "reject"
ID = "N26"
FEATURES = ["pax-global.path", "pax-global.empty-value.path"]


def build(a):
    a.pax([(b"path", b"global-name")], typeflag=b"g", name=b"pax_global_header",
          note="path=global-name, for every later member")
    a.pax([(b"path", b"")], typeflag=b"g", name=b"pax_global_header",
          note="path=, which removes the global path")
    a.file(b"a", b"which name?\n")
    a.end()

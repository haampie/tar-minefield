"""A global `path`, then a global header that removes it with an empty value.

The archive has a global header with `path=global-name`, then a second global header with an empty
`path=`, then a file whose header has the name `a`.

In [POSIX][global], the first applies to every later member, and the second [deletes][empty-value]
it again, so the file after them keeps the name in its header, `a`. POSIX deletes the global value
by name; whether the deletion also reaches the name in the header, as for an empty `path` in an
extended header, it leaves open, so the file may also be left without a name. This case is ambiguous
in practice because `path=` is also taken for an empty name, or ignored, so that the file is
`global-name`.

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

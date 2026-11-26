"""A pax `size` that disagrees with the header's, so that a reader of the header's misses a member.

The archive has a file `a` with size 512 in its ustar header and `size=0` in its pax header,
followed by an empty file `smuggled`.

In [POSIX][size-override], a pax `size` record overrides the ustar size field; this is how files
over 8 GiB, which do not fit in the ustar field, are archived, and writers place various placeholder
values in the ustar field. A compliant reader uses the pax size of 0 and reads the next block as
`smuggled`'s header. A reader that uses the ustar size or does not support pax consumes that block
as `a`'s data—the vulnerability in CVE-2025-62518 (astral-tokio-tar before 0.5.6 and tokio-tar).
Because POSIX requires [ignoring][corresponding] the ustar size when a pax `size` is present, the
default policy tolerates this archive. A stricter parser may still reject a small file whose pax and
ustar sizes disagree, provided it never extracts `a` with 512 bytes.

Decision point: which of two sizes frames the member.
Seen in: none of the scanned tarballs.
"""

VERDICT = "tolerate"
ID = "F14"
FEATURES = ["pax.size-disagrees"]
TREE = [
    {"path": "a", "kind": "file", "contents": b"", "executable": False},
    {"path": "smuggled", "kind": "file", "contents": b"", "executable": False},
]


def build(a):
    a.pax([(b"size", b"0")], note="size=0, for a")
    a.header(b"a", b"0", 512, note="size 512")
    a.file(b"smuggled", b"",
           note="the data of a, to an implementation that takes the header's size")
    a.end()

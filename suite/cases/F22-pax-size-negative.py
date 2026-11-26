"""A negative pax `size`, which a member cannot have.

The archive has a file `a` with `size=-512` in its pax header and size 0 in its ustar header,
followed by an empty file `smuggled`.

In [POSIX][size-decimal], a pax size consists of unsigned decimal digits, and POSIX does not say how
to handle a non-decimal `size` record. A reader that discards the invalid pax record falls back to
the ustar size of 0 and extracts `smuggled`, whereas one that parses `-512` into an unsigned integer
wraps it near 2^64 and reads past the end of the archive.

Decision point: whether a pax size may be negative, and what a negative one means.
Seen in: none of the scanned tarballs.
"""

VERDICT = "reject"
ID = "F22"
FEATURES = ["pax.invalid-size"]


def build(a):
    a.pax([(b"size", b"-512")], note="size=-512, for a")
    a.header(b"a", b"0", 0, note="size 0")
    a.file(b"smuggled", b"", note="a member, unless a reading of the pax size covers it")
    a.end()

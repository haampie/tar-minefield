"""Two `size` records in one pax header: first wins, or last wins?

The archive has a file `a` with size 0 in its ustar header and both `size=0` and `size=512` in its
pax header, followed by an empty file `smuggled`.

When records in the same pax header conflict, [POSIX][last-wins] gives precedence to the last one,
making `a`'s size 512 and the next block `a`'s data. A reader that keeps the first `size` record
uses 0 instead and reads the next block as `smuggled`'s header.

Decision point: which of two `size` records in one pax header takes effect.
Seen in: not measured, as earlier scanner versions did not record which key was repeated; the only
scanned tarball with a repeated pax key, libmygpo-qt 1.2.0, has no pax `size`.
See also: N20, two `path` records in one pax header, and F14, a pax `size` that disagrees with the
header.
"""

VERDICT = "reject"
ID = "F74"
FEATURES = ["pax.size-repeated", "pax.repeated-key"]


def build(a):
    a.pax([(b"size", b"0"), (b"size", b"512")], note="size=0, then size=512")
    a.header(b"a", b"0", 0)
    a.file(b"smuggled", b"", note="a's data if the last size wins")
    a.end()

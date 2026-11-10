"""A pax `size` twice in one header: the first, or the last?

The archive has a file `a`, whose pax header has the record `size=0` and then the record `size=512`,
and whose header has the size 0, then an empty file `smuggled`.

In [POSIX][last-wins], the last of conflicting records in one header takes precedence, so the size
is 512, and the next block is the data of `a`. This case is ambiguous in practice because a reader
that keeps the first record of a key reads 0, and the next block is the header of `smuggled`.

Decision point: which of two pax sizes in one header applies.
Seen in: not measured, as earlier versions of the scanner did not record which key a header has
twice: the one scanned tarball that has a key twice, libmygpo-qt 1.2.0, does not have a pax `size`.
See also: N20, a pax `path` twice in one header, and F14, a pax `size` that disagrees with the
header.
"""

VERDICT = "reject"
ID = "F74"
FEATURES = ["pax.size-repeated", "pax.repeated-key"]


def build(a):
    a.pax([(b"size", b"0"), (b"size", b"512")], note="two sizes")
    a.header(b"a", b"0", 0)
    a.file(b"smuggled", b"", note="the data of a, to a reader that takes the last size")
    a.end()

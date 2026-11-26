"""An archive that ends right after a file's data, without block padding.

The archive has a 5-byte file `a` and ends immediately after those 5 bytes, with no padding to 512
bytes and no zero blocks.

A POSIX archive consists of [512-byte blocks][block-512], and file data occupies [full
blocks][records-follow]. Even though all 5 bytes of `a` are present, the final block is incomplete.
A reader that reads only the file's byte count extracts `a` with its 5 bytes, sometimes without
reporting an error. A reader that requires full 512-byte blocks fails on the short read, leaving `a`
empty or unextracted.

Decision point: whether a file in an unpadded final block is extracted.
Seen in: not measured, as earlier scanner versions grouped this with archives missing the
end-of-archive marker; 22 scanned tarballs lack that marker and may end this way.
See also: F04, an archive that ends after a complete member, which is tolerated, and F08, one that
ends inside file data.
"""

VERDICT = "reject"
ID = "F63"
FEATURES = ["end.unpadded"]


def build(a):
    a.header(b"a", b"0", 5)
    a.cut(b"12345", "data: 5 bytes, which are not padded to a block")

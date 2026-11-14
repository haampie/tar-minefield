"""An archive that ends after the data of a file, before the end of its block.

The archive has a file `a` of 5 bytes, and ends right after those bytes, without padding to 512
bytes and without zero blocks.

In POSIX, an archive is a series of [blocks of 512 bytes][block-512], and the data of a file takes
[whole blocks][records-follow]. So this archive is cut short, although every byte of `a` is in it.
This case is ambiguous in practice because a reader that reads the data by its size extracts `a`
with its 5 bytes, and one that reads whole blocks cannot read the last one, and extracts an empty
`a`, or does not extract `a`. Most readers report an error. Some of those that extract the 5 bytes
do so without an error.

Decision point: whether a member whose last block is not complete is extracted.
Seen in: not measured, as earlier versions of the scanner took such an archive for one without an
end-of-archive marker: 22 of the scanned tarballs do not have that marker, and may end this way.
See also: F04, an archive that ends after a complete member, which is tolerated, and F08, one that
ends inside the data of a member.
"""

VERDICT = "reject"
ID = "F63"
FEATURES = ["end.unpadded"]


def build(a):
    a.header(b"a", b"0", 5)
    a.cut(b"12345", "data: 5 bytes, which are not padded to a block")

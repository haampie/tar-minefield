"""A checksum padded with spaces rather than zeros.

The archive has one file, `a`, with space-padded size and checksum fields: the checksum is
`" 10672\\0 "` (a leading space, five octal digits, a NUL, and a trailing space), and the size is
`"         15\\0"` (nine spaces, two octal digits, and a NUL).

The header bytes sum to the same value as a zero-padded header, so any implementation that accepts
the archive must extract `a`, including implementations that verify the checksum before parsing
other fields.

Decision point: whether the checksum field may start with a space.
Seen in: 819 release tarballs, among them 674 from CPAN, such as Starman 0.4015, and PyPDF2
1.26.0, which Spack fetches from PyPI: every tarball whose numeric fields are padded with spaces.
See also: F01, numeric fields padded with spaces, with a checksum as usual.
"""

VERDICT = "tolerate"
ID = "F32"
FEATURES = ["number.chksum.leading-space"]
TREE = [
    {"path": "a", "kind": "file", "contents": b"Archive::Tar\n", "executable": False},
]


def build(a):
    a.file(b"a", b"Archive::Tar\n", size=b"%11o\0" % 13, uname=b"perl", gname=b"perl",
           chksum="leading-space",
           note="the size and the checksum padded with spaces")
    a.end()

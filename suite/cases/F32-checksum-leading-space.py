"""A checksum padded with spaces rather than zeros, as Perl's `Archive::Tar` writes it.

F01 pads number fields with spaces but writes the checksum as usual. Real tarballs that pad with
spaces pad the checksum too: `Archive::Tar` writes it as `%6o\\0 `, which is a space, five octal
digits, a NUL and a space for the sums of real headers (`" 13312\\0 "`), and the size as spaces,
the digits and a NUL. The sum is the same as that of any other header, so every implementation must
extract `a`, also those that check the checksum before the other fields.

Decision point: whether the checksum field may start with a space.
Seen in: 819 source tarballs, 674 of them from CPAN, such as Starman 0.4015, and PyPDF2 1.26.0
from PyPI: every tarball whose number fields are padded with spaces.
"""

VERDICT = "accept"
ID = "F32"
TREE = [
    {"path": "a", "kind": "file", "contents": b"Archive::Tar\n", "executable": False},
]


def build(a):
    a.file(b"a", b"Archive::Tar\n", size=b"%11o\0" % 13, uname=b"perl", gname=b"perl",
           chksum="leading-space",
           note="the size and the checksum padded with spaces")
    a.end()

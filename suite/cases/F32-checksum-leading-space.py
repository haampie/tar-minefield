"""A checksum padded with spaces rather than zeros, as Perl's `Archive::Tar` writes it.

The archive has one file, `a`, whose size and checksum fields are padded with spaces, as Perl's
`Archive::Tar` writes them.

Tarballs that pad numeric fields with spaces pad the checksum too: `Archive::Tar` writes it as
`%6o\\0 `, which for a sum of five octal digits, as headers have, is a space, the digits, a NUL and
a space (`" 13312\\0 "`), and the size as spaces, the digits and a NUL. The sum is the same as that
of any other header, so an implementation that accepts the archive must extract `a`, also one that
checks the checksum before the other fields.

Decision point: whether the checksum field may start with a space.
Seen in: 819 release tarballs, 674 of them from CPAN, such as Starman 0.4015, and PyPDF2 1.26.0,
which Spack fetches from PyPI: every tarball whose numeric fields are padded with spaces.
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

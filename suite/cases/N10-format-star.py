r"""star's prefix field, which is shorter than ustar's.

star writes `tar\0` at the end of the header, and uses only part of ustar's prefix field for the
prefix, with times after it. In ustar, the prefix is the whole field. This case is ambiguous in
practice because the prefix is either the whole field, as ustar defines it, or its first part, as
star writes it.

Decision point: how long the prefix field is.
Seen in: berkeley-db 18.1.40 and ncurses 5.9.
"""

VERDICT = "reject"
ID = "N10"
FEATURES = ['format.star']


def build(a):
    a.file(b"a", b"a\n", prefix=b"dir", pad=b"\0\0\0\0\0\0\0\0tar\0", note="star's tar\\0 at offset 508")
    a.end()

r"""star's format with a short prefix, ended by a NUL and followed by star's times.

The archive has one file, `a`, whose prefix field has the prefix `dir`, followed by NULs to byte
131, followed by `15000000000 15000000000 `, which reads as two times; and whose header has `tar\0`
at offset 508, as star's own format puts it there.

star's own format splits the prefix field: 131 bytes for the prefix, then the access and change
times, in octal. star ends a prefix with a NUL, as here, so a reader that takes the prefix up to its
first NUL, [as POSIX does][prefix], reads the name `dir/a`, the same as a reader of star's format.

The bytes after that NUL are star's times, which a reader of the whole field takes into the name,
and then fails to create, so a strict parser rejects them rather than guess what they are for.

Decision point: whether the bytes after the NUL of a prefix count.
Seen in: berkeley-db 18.1.40 and ncurses 5.9, which are in star's format; the scan does not record
whether a member has a non-empty prefix.
See also: N10, a prefix that runs into star's times, and N14, bytes after the NUL of a name.
"""

VERDICT = "reject"
ID = "N34"
FEATURES = ["format.star"]


def build(a):
    # 155 bytes: the prefix and NULs to 131, then two numbers in the shape of star's times
    prefix = b"dir" + bytes(128) + b"15000000000 " + b"15000000000 "
    a.file(b"a", b"a\n", prefix=prefix, pad=b"\0" * 8 + b"tar\0",
           note="star's tar\\0 at offset 508")
    a.end()

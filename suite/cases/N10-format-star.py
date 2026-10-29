r"""A ustar prefix whose end reads as star's times, with star's `tar\0` at offset 508.

The archive has one file, `a`, whose prefix field fills all 155 bytes: 131 `p`s, then
`15000000000 15000000000 `, which reads as two times; and whose header has `tar\0` at offset 508,
as star's own format puts it there.

POSIX's ustar header ends at byte 500, with a prefix field of 155 bytes, which a prefix [may fill
without a NUL][name-full]. star's own format, xstar, puts `tar\0` at offset 508, in bytes that POSIX
leaves undefined, and splits the prefix field: 131 bytes for the prefix, then the access and change
times, in octal. star itself ends its prefixes with a NUL at byte 130, so that ustar readers read
them alike. This case is ambiguous because the prefix is either the whole field, which
[POSIX][prefix] joins to the name, or its first 131 bytes, as readers that recognize `tar\0` take
it: `a` is then under a directory whose name ends in those numbers, or of the 131 `p`s alone.

Decision point: whether `tar\0` at offset 508 makes the prefix field shorter.
Seen in: berkeley-db 18.1.40 and ncurses 5.9, which are in star's format; the scan does not
record whether a prefix runs past 130 bytes.
"""

VERDICT = "reject"
ID = "N10"
FEATURES = ['format.star']


def build(a):
    # 155 bytes: 131 for star's prefix, then two numbers in the shape of star's times
    prefix = b"p" * 131 + b"15000000000 " + b"15000000000 "
    a.file(b"a", b"a\n", prefix=prefix, pad=b"\0" * 8 + b"tar\0",
           note="star's tar\\0 at offset 508")
    a.end()

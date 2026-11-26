r"""A ustar prefix whose end reads as star's times, with star's `tar\0` at offset 508.

The archive has one file, `a`, with `tar\0` at offset 508 (as in star's format) and a 155-byte
prefix field containing 131 `p`s followed by `15000000000 15000000000 `.

A POSIX ustar header ends at byte 500 with a 155-byte prefix field, which a prefix [may fill
without a NUL][name-full]. In star's xstar format, bytes 508–511 hold `tar\0` and the 155-byte
prefix area is split into a 131-byte prefix followed by octal access and change times. When star
writes an xstar header, it always terminates the prefix with a NUL by byte 130 so ustar readers
parse the same prefix. Here there is no NUL: a standard [POSIX][prefix] reader uses all 155 bytes as
the directory name (including the trailing numbers), whereas a reader that recognizes `tar\0` uses
only the 131 `p`s.

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

"""A file mode encoded in base-256.

The archive has a file `a` whose mode field encodes octal 755 in base-256: a leading `0x80` byte
followed by a 7-byte big-endian integer.

GNU tar uses base-256 for numbers that overflow their octal field, such as large file sizes or user
IDs. Because a [12-bit mode][mode] always fits in four octal digits, archivers do not need base-256
for the mode field, and some readers support base-256 only for sizes or IDs. A reader that accepts
base-256 in every numeric field extracts `a` as executable. A reader that expects octal digits in
the mode field does not find any and extracts `a` as non-executable, while others report an error.

Decision point: whether base-256 encoding is accepted in the mode field.
Seen in: none of the scanned tarballs.
See also: F56, a size in base-256, and F80, a uid in base-256.
"""

VERDICT = "reject"
ID = "K13"
FEATURES = ["number.mode.base256"]


def build(a):
    a.file(b"a", b"a\n", mode=b"\x80" + (0o755).to_bytes(7, "big"), note="mode 755 in base-256")
    a.end()

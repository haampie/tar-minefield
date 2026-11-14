"""A mode in base-256.

The archive has a file `a`, whose mode field is 755 in base-256: the byte `0x80`, followed by the
number in binary.

In GNU's format, a number is written in base-256 when it does not fit in the octal digits of its
field, as a large size or uid does not. A [mode][mode] has 12 bits, which always fit, so writers do
not have a reason to write it in base-256, and not every reader of base-256 sizes reads base-256 in
a mode. This case is ambiguous in practice because a reader can take the field in one of three ways.
A reader that reads base-256 in every numeric field extracts `a` as an executable file. One that
reads base-256 only in some fields does not find octal digits in this one, and extracts `a` without
the execute permission. Other readers report an error.

Decision point: whether a mode may be in base-256.
Seen in: none of the scanned tarballs.
See also: F56, a size in base-256, and F80, a uid in base-256.
"""

VERDICT = "reject"
ID = "K13"
FEATURES = ["number.mode.base256"]


def build(a):
    a.file(b"a", b"a\n", mode=b"\x80" + (0o755).to_bytes(7, "big"), note="mode 755, in base-256")
    a.end()

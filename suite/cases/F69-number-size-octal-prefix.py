"""A size field starting with the octal prefix `0o`.

The archive has a file `a` with `0o000001000` in its size field, followed by an empty file
`smuggled`.

In [POSIX][zero-filled], numeric fields contain only leading-zero-filled octal digits, without a
prefix such as `0o`. A reader that accepts `0o` as an octal prefix, as Python's `int` does, parses
octal 1000 (512) and consumes the next block as `a`'s data. A reader that stops at the `o` parses
the leading `0` as size 0 and reads the next block as `smuggled`'s header.

Decision point: how a numeric field containing a letter is parsed.
Seen in: none of the scanned tarballs.
See also: F37, a size with the digit 9, and F51, a size with a plus sign.
"""

VERDICT = "reject"
ID = "F69"
FEATURES = ["number.size.invalid-character"]


def build(a):
    a.header(b"a", b"0", b"0o000001000\0", note="size 512 or 0")
    a.file(b"smuggled", b"", note="a's data if 0o is accepted")
    a.end()

"""A non-space byte after a checksum's NUL terminator, after the first member.

The archive has three files, `a`, `b` and `c`. In `b`'s 8-byte checksum field, six valid octal
digits and a NUL are followed by `x`.

POSIX numeric fields are [terminated][numeric] by one or more spaces or NULs, and writers
conventionally end the 8-byte checksum field with a NUL and a space. POSIX does not specify whether
arbitrary bytes may follow a NUL terminator. A reader that stops at the NUL accepts the checksum and
extracts `a`, `b` and `c`. A reader that validates all 8 bytes of the field rejects `b`'s header: if
it then scans forward for the next valid header, it extracts only `a` and `c`; otherwise it reports
an error.

Decision point: whether bytes after a checksum's NUL terminator are checked.
Seen in: not measured, as earlier scanner versions did not record it; 7 scanned tarballs have a
checksum byte other than an octal digit, space or NUL.
See also: F47, a bad checksum after the first member, and F32, a space-padded checksum.
"""

VERDICT = "reject"
ID = "F76"
FEATURES = ["number.chksum.invalid-character"]


def build(a):
    a.file(b"a", b"a\n")
    a.file(b"b", b"b\n", chksum=lambda total: b"%06o\0x" % total,
           note="checksum ends with NUL and x")
    a.file(b"c", b"c\n")
    a.end()

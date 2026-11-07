r"""A symlink whose target in the header is not UTF-8.

The archive has a symlink `link`, whose header has the target `caf\xe9`, `café` in Latin-1, and
which does not have a pax header.

The fields of a ustar header are bytes, and in [POSIX][ascii-header] the characters of a header are
those of ISO/IEC 646, of which `\xe9` is not one, so the archive does not conform, and the encoding
of other characters in names is [implementation-defined][name-encoding]. A reader decodes the target
as UTF-8, as another encoding, or not at all. This case is ambiguous because the target is either
the bytes as they are, `caf\xe9`, or a decoding of them, such as `café` or `caf` followed by U+FFFD.

Decision point: how a link target that is not UTF-8 is decoded.
Seen in: none of the scanned tarballs.
See also: N31, the same target in a pax `linkpath`, and N18, a name that is not UTF-8.
"""

VERDICT = "reject"
ID = "N32"
FEATURES = ["linkname.not-utf8"]


def build(a):
    a.symlink(b"link", b"caf\xe9", note="a target that is not UTF-8")
    a.end()

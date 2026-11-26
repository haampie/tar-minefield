r"""A symlink whose target in the header is not UTF-8.

The archive has a symlink `link` with the Latin-1 target `caf\xe9` (`café`) in its ustar linkname
field and no pax header.

In [POSIX][ascii-header], ustar header characters come from ISO/IEC 646 (ASCII), and the encoding of
other bytes in names is [implementation-defined][name-encoding]. Depending on whether and how the
reader decodes the field, the extracted link target is the raw bytes `caf\xe9`, `café` (decoded from
Latin-1), or `caf` followed by U+FFFD.

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

r"""A size in the header of a hardlink, in a pax archive, which takes the next header for its data.

The archive has a file `a`, then a hardlink `h` to `a`, with a pax header and the size 512 in its
header, then an empty file `smuggled`.

Read as pax, which its `x` header suggests, data on a hardlink is [permitted][link-data], so the
block after the header of `h` is its data, and what looks like the header of `smuggled` is that
data. POSIX does not say what the data of a hardlink does: whether it replaces the contents of `a`,
or is ignored. A reader that reads it as ustar, in which [no data][no-data] is stored for a hard
link, reads `smuggled` as a member; the bytes do not say which it is. This case is ambiguous because
the tree has `a` and its link `h`, which contain `a\n` or that block, or `a`, `h` and `smuggled`.

Decision point: whether a size in the header of a hardlink applies, in an archive with pax headers.
Seen in: none of the scanned tarballs.
See also: F33, a size in the header of a directory, F35, a pax size on a hardlink, and F38, the same
in an archive without pax headers.
"""

VERDICT = "reject"
ID = "F34"
FEATURES = ["size.on-hardlink"]


def build(a):
    a.file(b"a", b"a\n")
    a.pax([(b"mtime", b"1")], note="for h, which makes the archive pax")
    a.header(b"h", b"1", 512, note="a hardlink to a, with a size of 512", linkname=b"a")
    a.file(b"smuggled", b"", note="the block that the size covers")
    a.end()

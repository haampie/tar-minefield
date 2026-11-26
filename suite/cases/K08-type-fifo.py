"""A FIFO member: created, extracted as an empty file, or skipped?

The archive has a FIFO `p` (typeflag `6`), followed by a file `b`.

In POSIX, typeflag `6` represents a FIFO, which [does not store contents][fifo]. If a reader cannot
create the FIFO, it [must report an error][cannot-create]; only unknown file types that can carry
data are [extracted as regular files][unknown-type]. The test suite's tree model includes only
files, directories and links, not FIFOs. A reader that supports FIFOs creates `p` as a FIFO. A
reader that extracts any non-directory, non-link member as a regular file creates an empty file `p`,
while one that skips unsupported member types extracts only `b`. Other readers report an error.

Decision point: how a reader handles a member that is not a file, directory or link.
Seen in: not measured, as earlier scanner versions did not flag it as a feature; the scanner did
record member kinds, and one tarball, forktty 1.3, contains a FIFO.
See also: F16, an unknown typeflag.
"""

VERDICT = "reject"
ID = "K08"
FEATURES = ["type.fifo"]


def build(a):
    a.header(b"p", b"6", 0, note="FIFO")
    a.file(b"b", b"b\n")
    a.end()

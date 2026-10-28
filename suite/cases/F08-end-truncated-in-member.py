"""An archive that ends inside the data of a member.

The size field in the header of `a` is 1024, but the archive ends after 512 bytes of its data.

Decision point: whether a member that is cut short is extracted.
Seen in: none of the scanned tarballs.
See also: F04, an archive cut short after a complete member, or one without an end-of-archive
marker, which is tolerated.
"""

VERDICT = "reject"
ID = "F08"
FEATURES = []


def build(a):
    a.header(b"a", b"0", 1024, note="size 1024")
    a.raw(b"x" * 512, "data: the first 512 of the 1024 bytes, and then the file ends")

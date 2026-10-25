"""Another archive after the end-of-archive marker.

The archive ends with two zero blocks, as it should, and is followed by a second archive with a file
`hidden`. In POSIX, the archive ends at the marker, and `hidden` is not part of it. This case is
ambiguous in practice because reading on past the marker, as GNU tar does with `--ignore-zeros`,
extracts `hidden` as well.

Decision point: whether an implementation stops at the end-of-archive marker.
Seen in: glibmm 2.16.0, which is the whole archive twice, jmol 14.8.0 and commons-jexl 2.1.1.
See also: F02, junk after the two zero blocks, which is tolerated.
"""

VERDICT = "reject"
ID = "F07"
FEATURES = ['end.archive-after']
POSIX = "end"


def build(a):
    a.file(b"a", b"a\n")
    a.end()
    a.file(b"hidden", b"seen by readers that read past the end-of-archive marker\n")
    a.end()

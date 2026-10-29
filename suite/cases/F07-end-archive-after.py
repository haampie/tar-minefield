"""Another archive after the end-of-archive marker.

The archive ends with two zero blocks, as it should, and is followed by a second archive with a file
`hidden`. In [POSIX][end], the archive ends at the marker, and `hidden` is not part of it. This case
is ambiguous in practice because a reader that reads on past the marker, by default or with an
option, extracts `hidden` as well.

Decision point: whether an implementation stops at the end-of-archive marker.
Seen in: glibmm 2.16.0, whose second archive, in GNU's format, has the files of the first and 6
more with long names, jmol 14.8.0, and commons-jexl 2.1.1, whose record after the marker holds
stale copies of headers before it.
See also: F02, junk after the two zero blocks, which is tolerated.
"""

VERDICT = "reject"
ID = "F07"
FEATURES = ['end.archive-after']


def build(a):
    a.file(b"a", b"a\n")
    a.end()
    a.file(b"hidden", b"seen by readers that read past the end-of-archive marker\n")
    a.end()

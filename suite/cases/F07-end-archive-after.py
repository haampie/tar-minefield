"""Another archive after the end-of-archive marker.

The archive has a file `a` followed by the two zero blocks that end the archive, and then a second
archive containing a file `hidden`.

In [POSIX][end], the archive ends at the two zero blocks, so `hidden` is not part of it. However, a
reader that continues reading past the end-of-archive marker, either by default or via an option,
extracts `hidden` as well.

Decision point: whether an implementation stops at the end-of-archive marker.
Seen in: glibmm 2.16.0 (whose second archive, in GNU format, repeats the files of the first plus 6
more with long names), jmol 14.8.0, and commons-jexl 2.1.1 (whose trailing blocks contain stale
copies of earlier headers).
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

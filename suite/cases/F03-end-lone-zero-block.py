"""An end-of-archive marker of one zero block, not two.

[POSIX][end] requires two zero blocks at the end of an archive; most implementations stop at the
first, so they extract it all the same.

Decision point: whether one zero block is an end-of-archive marker.
Seen in: eng-rus, srecord 1.64 and cdi2iso 0.1.
See also: F09, one zero block followed by another member, which is rejected as well.
"""

VERDICT = "reject"
ID = "F03"
FEATURES = ['end.lone-zero-block']


def build(a):
    a.file(b"a", b"a\n")
    a.zeros(1, note="one zero block, and the file ends")

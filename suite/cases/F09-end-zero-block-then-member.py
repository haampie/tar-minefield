"""A zero block, then another member: the end of the archive, or not?

POSIX requires two zero blocks at the end of an archive, so one zero block is neither a header nor
the end-of-archive marker. Here it is followed by a file, `hidden`. Read leniently, this case is
ambiguous because the zero block either ends the archive, or is skipped, and only in the second
reading is `hidden` extracted.

Decision point: whether one zero block ends the archive.
Seen in: 7 tarballs that `tarscan.py` counts, such as jakarta-oro 2.0.8 and commons-cli 1.2-src,
but in none of them is the zero block followed by a member: what follows is not a valid header,
and in those two, it is stale data, as after F03.
See also: F03, one zero block with nothing after it, which is rejected as well.
"""

VERDICT = "reject"
ID = "F09"
FEATURES = ['end.zero-block-before-member']
POSIX = "end"


def build(a):
    a.file(b"a", b"a\n")
    a.zeros(1, note="a lone zero block")
    a.file(b"hidden", b"seen by readers that read past a zero block\n")
    a.end()

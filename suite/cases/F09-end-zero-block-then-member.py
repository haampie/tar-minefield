"""A zero block, then another member: the end of the archive, or not?

The archive has a file `a`, a single zero block, a file `hidden`, and finally the two zero blocks
that end the archive.

In [POSIX][end], an archive ends with two zero blocks, so a single zero block is neither a valid
header nor a complete end-of-archive marker. A reader that treats a lone zero block as the end of
the archive stops after `a`, whereas one that skips a single zero block continues and extracts
`hidden`.

Decision point: whether one zero block ends the archive.
Seen in: 7 tarballs have a zero block followed by non-zero blocks, such as jakarta-oro 2.0.8 and
commons-cli 1.2-src, though in none of them is the zero block followed by a valid header (in those
two, it is followed by stale data).
See also: F03, one zero block with nothing after it, which is rejected as well.
"""

VERDICT = "reject"
ID = "F09"
FEATURES = ['end.zero-block-before-member']


def build(a):
    a.file(b"a", b"a\n")
    a.zeros(1, note="a lone zero block")
    a.file(b"hidden", b"seen by readers that read past a zero block\n")
    a.end()

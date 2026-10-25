"""A zero block, then another member: the end of the archive, or not?

POSIX requires two zero blocks at the end of an archive, and GNU tar stops at the first zero block
it reads by default, while `--ignore-zeros` reads on. After one zero block comes a file, `hidden`,
which some implementations extract and others never see.

Decision point: whether one zero block ends the archive.
Seen in: jakarta-oro 2.0.8, PullParser 2.1.10 and commons-cli 1.2-src.
"""

VERDICT = "reject"
ID = "F09"
FEATURES = ['end.zero-block-before-member']


def build(a):
    a.file(b"a", b"a\n")
    a.zeros(1, note="a lone zero block")
    a.file(b"hidden", b"seen by readers that read past a zero block\n")
    a.end()

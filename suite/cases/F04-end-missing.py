"""No end-of-archive marker: the archive ends after a complete member.

POSIX requires two zero blocks at the end of an archive. Without them, an archive cannot be told
apart from one cut short after a member.

Decision point: whether an archive without an end-of-archive marker is complete.
Seen in: SDL2_image 2.8.8, ruby 4.0.5 and fastcap 2.0-18Sep92.
See also: F08, an archive cut short inside the data of a member, which is rejected as well.
"""

VERDICT = "reject"
ID = "F04"
FEATURES = ['end.missing']
POSIX = "end"


def build(a):
    a.file(b"a", b"a\n")

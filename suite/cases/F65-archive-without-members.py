"""An archive without members: only the two zero blocks that end it.

The archive has the end-of-archive marker, two zero blocks, without a member before it.

In [POSIX][end], an archive ends with two zero blocks, and a member before them is not required. GNU
tar writes such an archive for an empty list of files, and RubyGems for a gem without files. The
tree is empty.

Seen in: 38 gems that do not have files, such as lil 0.0.4 and slds 0.1.1.
See also: F66, a file of 0 bytes, which is rejected.
"""

VERDICT = "accept"
ID = "F65"
FEATURES = []
TREE = []


def build(a):
    a.end()

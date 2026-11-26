"""An archive with no members, containing only the two trailing zero blocks.

The archive consists solely of the end-of-archive marker: two 512-byte zero blocks, with no members.

In [POSIX][end], an archive ends with two zero blocks and need not contain any members. GNU tar
writes such an archive when given an empty file list, as does RubyGems for a gem with no files. The
extracted tree is empty.

Seen in: 38 gems with no files, such as lil 0.0.4 and slds 0.1.1.
See also: F66, a zero-byte file, which is rejected.
"""

VERDICT = "accept"
ID = "F65"
FEATURES = []
TREE = []


def build(a):
    a.end()

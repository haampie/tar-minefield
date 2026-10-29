"""The same file twice, with the same contents.

The archive has two files named `a`, with the same contents.

Whichever copy is kept, the tree is the same. But an extractor that streams the archive cannot know,
when it writes the first copy, whether a later one is the same: a duplicate with the same contents
and one with other contents look alike until the end.

Decision point: which of two members of one path is the file.
Seen in: tarballs of `cabal sdist`, such as string-conversions 0.4.0.1 and multipart 0.2.1.
See also: S07, the same file twice, with different contents.
"""

VERDICT = "reject"
ID = "S09"
FEATURES = ['tree.duplicate.file-file']


def build(a):
    a.file(b"a", b"same\n")
    a.file(b"a", b"same\n")
    a.end()

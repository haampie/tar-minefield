r"""A control character in a name, here a newline.

The name `a\nb` is valid on Unix. This case is ambiguous because, read line by line, as listings,
manifests and scripts do, the one name is two, `a` and `b`.

Decision point: whether a name may contain control characters.
Seen in: cdrtools 3.02a09, wgrib2 3.6.0 and apktool 2.6.0.
"""

VERDICT = "reject"
ID = "N15"
FEATURES = ['name.control-character']


def build(a):
    a.file(b"a\nb", b"a newline in my name\n")
    a.end()

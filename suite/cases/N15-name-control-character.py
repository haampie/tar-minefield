r"""A control character in a name, here a newline.

The name `a\nb` is valid on Unix, but listings, manifests and scripts that read names line by line
see two names. Every implementation that accepts the archive extracts `a\nb`: the case is rejected
because of those tools, not because it is ambiguous.

Decision point: whether a name may contain control characters.
Seen in: cdrtools 3.02a09, wgrib2 3.6.0 and apktool 2.6.0.
"""

VERDICT = "reject"
ID = "N15"
FEATURES = ['name.control-character']


def build(a):
    a.file(b"a\nb", b"a newline in my name\n")
    a.end()

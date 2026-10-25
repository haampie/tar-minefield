r"""A control character in a name, here a newline.

The name `a\nb` is valid on Unix. This case is ambiguous because the member can look like two
separate files, `a` and `b`, as in the output of `ls` piped to another command, in manifests and in
scripts.

Decision point: whether a name may contain control characters.
Seen in: cdrtools 3.02a09, wgrib2 3.6.0 and apktool 2.6.0.
"""

VERDICT = "reject"
ID = "N15"
FEATURES = ['name.control-character']


def build(a):
    a.file(b"a\nb", b"a newline in my name\n")
    a.end()

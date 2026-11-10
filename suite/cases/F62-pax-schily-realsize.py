"""A `SCHILY.realsize` record on a file that is not sparse.

The archive has a file `a` of 5 bytes, `12345`, whose pax header has the record `SCHILY.realsize=2`.

In star's format of sparse files, whose holes are not stored, the size of a file with its holes is
in `SCHILY.realsize`, and the size field is that of the data that is stored. In
[POSIX][keyword-extension], such a key is an implementation extension, which another reader need not
know. The file `a` is not sparse: the archive does not have a list of its holes. This case is
ambiguous in practice because a reader that does not know the key extracts the 5 bytes, and one that
takes the real size for the size of the file extracts its first 2 bytes, `12`.

Decision point: whether `SCHILY.realsize` applies to a file that is not sparse.
Seen in: none of the scanned tarballs.
See also: N36, GNU's pax keys of sparse files.
"""

VERDICT = "reject"
ID = "F62"
FEATURES = ["pax.SCHILY.realsize"]


def build(a):
    a.pax([(b"SCHILY.realsize", b"2")], note="a real size of 2")
    a.file(b"a", b"12345")
    a.end()

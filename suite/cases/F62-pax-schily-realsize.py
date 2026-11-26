"""A `SCHILY.realsize` pax record on a non-sparse file.

The archive has a 5-byte file `a` containing `12345`, preceded by a pax header with
`SCHILY.realsize=2`.

In star's sparse format, `SCHILY.realsize` holds the file's full size including holes, while the
header's size field gives the stored data size. Under [POSIX][keyword-extension], this key is a
vendor extension that other readers need not recognize. Here `a` is a regular file with no hole map.
A reader that ignores `SCHILY.realsize` extracts all 5 bytes, whereas one that applies it truncates
the file to its first 2 bytes, `12`.

Decision point: whether `SCHILY.realsize` applies to a non-sparse file.
Seen in: none of the scanned tarballs.
See also: N36, GNU sparse pax keys.
"""

VERDICT = "reject"
ID = "F62"
FEATURES = ["pax.SCHILY.realsize"]


def build(a):
    a.pax([(b"SCHILY.realsize", b"2")], note="SCHILY.realsize=2")
    a.file(b"a", b"12345")
    a.end()

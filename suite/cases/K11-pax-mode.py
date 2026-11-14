"""A pax `mode` record on a file.

The archive has a file `a` with the mode 644, whose pax header has the record `mode=0755`.

In POSIX, the keyword `mode` is not specified for pax records: the [12 bits][mode] of a mode always
fit in the header. As a keyword of lowercase letters, it is [reserved][keyword-reserved] for future
standardization. This case is ambiguous because a reader either does not know the keyword, and
extracts `a` with the mode of its header, or applies it, and makes `a` executable. A reader that
applies it can read `0755` as octal, as the mode field is, or as decimal, as the other numbers of
pax records are.

Decision point: whether a pax `mode` record applies.
Seen in: not measured, as the scans do not record all pax keys of a tarball, only its 8 most common:
the key `mode` is not among those of any tarball, and 9 of the scanned tarballs have more keys.
See also: K09, an executable file.
"""

VERDICT = "reject"
ID = "K11"
FEATURES = ["pax.mode"]


def build(a):
    a.pax([(b"mode", b"0755")], note="a mode, which is not a keyword of POSIX")
    a.file(b"a", b"a\n")
    a.end()

"""A non-standard pax `mode` record on a file.

The archive has a file `a` with mode 644 in its ustar header and `mode=0755` in its pax header.

POSIX does not define a `mode` keyword for pax extended headers because the [12 mode bits][mode]
always fit in the ustar field; as a lowercase name, `mode` is [reserved][keyword-reserved] for
future standardization. A reader that ignores unknown keywords extracts `a` with mode 644, whereas
one that honors `mode=0755` makes `a` executable (parsing `0755` either as octal, like the ustar
mode field, or as decimal, like standard numeric pax records).

Decision point: whether a pax `mode` record overrides the ustar mode field.
Seen in: not measured, as the scanner records only the 8 most common pax keys per tarball; `mode` is
not among them in any tarball, and 9 scanned tarballs have additional keys.
See also: K09, an executable file.
"""

VERDICT = "reject"
ID = "K11"
FEATURES = ["pax.mode"]


def build(a):
    a.pax([(b"mode", b"0755")], note="non-standard pax mode=0755")
    a.file(b"a", b"a\n")
    a.end()

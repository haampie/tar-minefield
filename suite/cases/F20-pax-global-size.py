"""A global pax header with a `size`, which frames every member after it, or none.

The archive starts with a global header with `size=512`, then has a file `a`, whose size field is
0, then an empty file `smuggled`.

In [POSIX][global], the records of a global header apply to every later member that does not
override them, so the `size=512` is the size of `a`. This case is ambiguous in practice because,
with global headers or the sizes in them ignored, the next block is not the data of `a` but the
header of another file, `smuggled`. A reader may also do both: give `a` and `smuggled` the global
size, but read the header of `smuggled` right after that of `a`, so that the data of `a` is that
header.

Decision point: whether a `size` in a global header applies.
Seen in: none of the scanned tarballs.
"""

VERDICT = "reject"
ID = "F20"
FEATURES = ["pax-global.size"]


def build(a):
    a.pax([(b"size", b"512")], typeflag=b"g", name=b"pax_global_header", note="size=512")
    a.header(b"a", b"0", 0, note="size 0, but the global size is 512")
    a.file(b"smuggled", b"", note="the data of a, to an implementation that applies the global size")
    a.end()

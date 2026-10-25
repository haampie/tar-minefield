"""A global pax header with a `size`, which frames every member after it, or none.

In POSIX, the records of a global header apply to every later member that does not override them, so
the `size=512` of this one is the size of `a`, whose header says 0. No archiver writes a size in a
global header. This case is ambiguous in practice because, with global headers or the sizes in them
ignored, the next block is not the data of `a` but the header of another file, `smuggled`.

Decision point: whether a `size` in a global header applies.
Seen in: no source tarball.
"""

VERDICT = "reject"
ID = "F20"
FEATURES = ["pax-global.size"]


def build(a):
    a.pax([(b"size", b"512")], typeflag=b"g", name=b"pax_global_header", note="size=512")
    a.header(b"a", b"0", 0, note="size 0, but the global size says 512")
    a.file(b"smuggled", b"", note="the data of a, to an implementation that applies the global size")
    a.end()

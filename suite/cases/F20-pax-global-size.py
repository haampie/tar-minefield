"""A global pax header with a `size`, which frames every member after it, or none.

The archive starts with a global header containing `size=512`, followed by a file `a` with size 0 in
its ustar header, and then an empty file `smuggled`.

In [POSIX][global], global header records apply to every subsequent file that does not override
them, giving `a` a size of 512 and making the next block `a`'s data. A reader that ignores global
headers or ignores `size` in a global header uses `a`'s ustar size of 0 and reads the next block as
`smuggled`'s header.

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

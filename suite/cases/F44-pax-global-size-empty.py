"""An empty `size` in a global pax header: does it delete the size of every later member, or set it?

The archive has a global header, typeflag `g`, with the one record `size=`, then a file `a` with the
size 512 in its header, then an empty file `smuggled`.

In [POSIX][empty-value], a record with an empty value deletes any header block field of the same
name, and a value in a global header [applies][global] to every file after it. So `size=` can be
seen as deleting the size of `a`, whose size in the header is then [ignored][corresponding], so that
`a` does not have a size. It can also be seen as an empty size, [assigned][g-assigned] to `a`, or as
a record that deletes only earlier global values, so that the size in the header stands. This case
is ambiguous because `a` does not have a size (and is invalid), the size 0 (and `smuggled` is a
member), or the size 512 (and the next block is its data).

Decision point: what an empty size in a global header deletes.
Seen in: none of the scanned tarballs.
See also: F20, a size in a global header, and F21, an empty size in an extended header.
"""

VERDICT = "reject"
ID = "F44"
FEATURES = ["pax-global.empty-value.size"]


def build(a):
    a.pax([(b"size", b"")], typeflag=b"g", name=b"pax_global_header",
          note="size=, which deletes the size of every later member")
    a.header(b"a", b"0", 512, note="size 512")
    a.file(b"smuggled", b"", note="the data of a, to a reader that keeps its size")
    a.end()

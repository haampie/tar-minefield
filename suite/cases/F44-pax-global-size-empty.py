"""An empty `size` in a global pax header: does it delete the size of every later member, or set it?

The archive has a global header, typeflag `g`, with the one record `size=`, then a file `a` with the
size 512 in its header, then an empty file `smuggled`.

[POSIX][empty-value] says that a record with an empty value deletes any header block field of the
same name, and a value in a global header [applies][global] to every file after it. So `size=`
deletes the size of `a`, and the size in its header is to be [ignored][corresponding], which leaves
`a` without a size, which POSIX does not define. But its order of precedence [assigns][g-assigned]
the empty value, which is not a number, or 0 to a lenient reader, or, [failing
that][header-fallback], the size in the header of `a`, 512, which takes the next block for its
data. This case is ambiguous because the tree has `a` with that block as its contents, an empty `a`
and `smuggled`, or no tree.

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

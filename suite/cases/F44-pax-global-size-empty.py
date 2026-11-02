"""An empty `size` in a global pax header, which in POSIX deletes the size of every later member.

The archive has a global header, typeflag `g`, with the one record `size=`, then a file `a` with the
size 512 in its header, then an empty file `smuggled`.

[POSIX][empty-value] says that a record with an empty value deletes any header block field of the
same name, and a value in a global header [applies][global] to every file after it. So `size=`
deletes the size of `a`, and leaves it without one, which POSIX does not define. A reader that
ignores the record, or deletes only a size that an extended header gave, reads 512 from the header
of `a`, and takes the next block for its data. This case is ambiguous because the tree has `a` with
that block as its contents, an empty `a` and `smuggled`, or no tree, as the size of `a` is gone.

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

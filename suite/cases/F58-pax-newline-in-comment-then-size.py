r"""A newline in a pax `comment`, which split on lines leaves a `size` record before the last one.

The archive has a file `a` with size 512 in its ustar header and two records in its pax header: a
`comment` containing `x\n10 size=0`, followed by `size=512`. The 512-byte data block of `a` is a
valid header for an empty file `smuggled`.

Because pax records are delimited by their [byte length][record-length], the comment is a single
record that [POSIX][comment] ignores, and `size=512` [overrides][size-override] the ustar size
field, giving `a` the 512-byte block as its contents. A reader that splits the pax payload on
newlines sees a `size=0` record before `size=512`; if it also takes the first `size` record instead
of the [last][last-wins], it extracts an empty `a` followed by `smuggled`.

Seen in: none of the scanned tarballs.
See also: F28, a `size` record in a comment on a file without a pax size.
"""

from blocks import Archive
F = lambda path, contents: {"path": path, "kind": "file", "contents": contents, "executable": False}

# The data of a: the bytes of a header of an empty file
SMUGGLED = Archive().header(b"smuggled", b"0", 0).bytes()

VERDICT = "accept"
ID = "F58"
FEATURES = ["pax.newline-in-value.comment"]
TREE = [F("a", SMUGGLED)]


def build(a):
    a.pax([(b"comment", b"x\n10 size=0"), (b"size", b"512")],
          note="a comment with a newline, then size=512")
    a.header(b"a", b"0", 512, note="size 512")
    a.file(b"smuggled", b"", note="the data of a")
    a.end()

r"""A newline in a pax `comment`, which split on lines leaves a `size` record before the real one.

The archive has a file `a`, whose pax header has a `comment` with a newline in it, `x\n10 size=0`,
then the record `size=512`, and whose header has the size 512 too. The 512 bytes after the header
are the header of an empty file `smuggled`.

pax records are delimited by their [length][record-length], so the comment is one record, which is
[ignored][comment], and the pax size [overrides][size-override] the size field: `a` contains the
512 bytes. This case is not ambiguous. A reader that splits records on lines finds a record
`size=0` before `size=512`, and one that takes the first, rather than the [last][last-wins],
extracts an empty `a`, then `smuggled`, but POSIX has no such reading.

Seen in: none of the scanned tarballs.
See also: F28, a `size` record in a comment on a file without a pax size.
"""

from blocks import Archive
F = lambda path, contents: {"path": path, "kind": "file", "contents": contents, "executable": False}

# The data of a: the bytes of a header of an empty file
SMUGGLED = Archive().header(b"smuggled", b"0", 0).bytes()

VERDICT = "accept"
ID = "F59"
FEATURES = ["pax.newline-in-value.comment"]
TREE = [F("a", SMUGGLED)]


def build(a):
    a.pax([(b"comment", b"x\n10 size=0"), (b"size", b"512")],
          note="a comment with a newline, then size=512")
    a.header(b"a", b"0", 512, note="size 512")
    a.file(b"smuggled", b"", note="the data of a")
    a.end()

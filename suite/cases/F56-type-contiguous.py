"""A contiguous file, typeflag `7`.

The archive has one member, `a`, of typeflag `7`, whose data is `a`, followed by a newline.

In POSIX, typeflag `7` is reserved for a file with some [high-performance
attribute][high-performance]. This [means a contiguous file][contiguous-files]: a file stored in
consecutive blocks on disk. [Implementations without such extensions][contiguous] should treat it as
a regular file. A reader that does not recognize typeflag `7` extracts it [as a regular
file][unknown-type] too. This case is tolerated because that is its one reading: as a regular file,
or as a contiguous file where they are supported, the file is `a` with its data. A strict parser may
reject it, as it may any typeflag it does not support; a reader that skips such a typeflag extracts
nothing.

Seen in: none of the scanned tarballs.
See also: F16, an unknown typeflag with a size.
"""
F = lambda path, contents: {"path": path, "kind": "file", "contents": contents, "executable": False}

VERDICT = "tolerate"
ID = "F56"
FEATURES = ["type.contiguous"]
TREE = [F("a", b"a\n")]


def build(a):
    a.header(b"a", b"7", 2, note="a contiguous file")
    a.data(b"a\n")
    a.end()

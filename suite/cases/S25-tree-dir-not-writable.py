"""A read-only directory member followed by a file inside it.

The archive has a directory `d/` with mode 555, followed by a file `d/f`.

Archiving a read-only directory with `tar cf x.tar d` writes the directory header (with mode 555)
before the files inside it. An unprivileged reader that applies mode 555 immediately upon creating
`d` cannot create `d/f`. As the [POSIX rationale][dir-permissions] notes, an extractor should create
directories with write permission and defer applying their archived modes until extraction finishes.
Directory modes are not part of the expected tree, which consists of `d` and `d/f`.

Seen in: not measured, as the scanner does not record directory modes.
See also: S01, a directory member after its contents.
"""
F = lambda path, contents: {"path": path, "kind": "file", "contents": contents, "executable": False}
D = lambda path: {"path": path, "kind": "directory"}

VERDICT = "accept"
ID = "S25"
FEATURES = []
TREE = [D("d"), F("d/f", b"f\n")]


def build(a):
    a.directory(b"d/", mode=0o555, note="read-only")
    a.file(b"d/f", b"f\n")
    a.end()

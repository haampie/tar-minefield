"""Files executable by their group or others, but not by their owner.

The archive has two files: `g`, with the mode 654, and `o`, with the mode 645.

The [mode][mode] field contains an execute permission for the owner of a file, one for its group,
and one for others. In the tree, a file is executable if its owner may execute it, and here the
owner may not, so neither file is executable. A reader that takes any of the three permissions for
that of the owner makes both executable.

Seen in: not measured, as the scans do not record modes.
See also: K09, an executable file.
"""
F = lambda path, contents: {"path": path, "kind": "file", "contents": contents, "executable": False}

VERDICT = "accept"
ID = "K10"
FEATURES = []
TREE = [F("g", b"g\n"), F("o", b"o\n")]


def build(a):
    a.file(b"g", b"g\n", mode=0o654, note="executable by its group only")
    a.file(b"o", b"o\n", mode=0o645, note="executable by others only")
    a.end()

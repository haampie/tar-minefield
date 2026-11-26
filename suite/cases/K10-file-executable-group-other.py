"""Files executable by group or others, but not by their owner.

The archive has two files: `g` with mode 654, and `o` with mode 645.

The [mode][mode] field has separate execute bits for the file's owner, its group, and others. In the
expected tree, a file counts as executable only when the owner execute bit is set, so neither `g`
nor `o` is executable. A reader that checks whether any of the three execute bits is set makes both
files executable for the owner.

Seen in: not measured, as the scanner does not record file modes.
See also: K09, an executable file.
"""
F = lambda path, contents: {"path": path, "kind": "file", "contents": contents, "executable": False}

VERDICT = "accept"
ID = "K10"
FEATURES = []
TREE = [F("g", b"g\n"), F("o", b"o\n")]


def build(a):
    a.file(b"g", b"g\n", mode=0o654, note="executable by group only")
    a.file(b"o", b"o\n", mode=0o645, note="executable by others only")
    a.end()

"""A symlink with an empty linkname field and a pax `linkpath`.

The archive has a symlink `l`, whose pax header has `linkpath=target`, and whose header has an empty
linkname field.

The pax `linkpath` [overrides][linkpath] the linkname field, so the empty field is not used, and
`l` points to `target`.

Seen in: none of the scanned tarballs.
See also: N34, an empty pax `linkpath`.
"""
L = lambda path, target: {"path": path, "kind": "symlink", "target": target}

VERDICT = "accept"
ID = "N46"
FEATURES = []
TREE = [L("l", "target")]


def build(a):
    a.pax([(b"linkpath", b"target")])
    a.symlink(b"l", b"", note="an empty linkname field")
    a.end()

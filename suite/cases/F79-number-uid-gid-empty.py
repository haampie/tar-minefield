"""Uid and gid fields without digits, as the writers of most crates leave them.

The archive has a file `a` with GNU's magic, whose uid and gid fields are 8 NULs each.

In [POSIX][uid-gid], these fields are the owner and the group of a file, which are not part of the
tree, and as [numeric fields][zero-filled] they are octal numbers, which an empty field is not.
Writers that do not record an owner leave them empty all the same, and a reader takes an empty field
for 0, or does not read it.

Seen in: 5,394 of the scanned tarballs, most of them crates.
"""
F = lambda path, contents: {"path": path, "kind": "file", "contents": contents, "executable": False}

VERDICT = "accept"
ID = "F79"
FEATURES = ["number.uid.no-digits", "number.gid.no-digits"]
TREE = [F("a", b"a\n")]


def build(a):
    a.file(b"a", b"a\n", uid=b"\0", gid=b"\0", magic=b"ustar ", version=b" \0",
           note="uid and gid of NULs")
    a.end()

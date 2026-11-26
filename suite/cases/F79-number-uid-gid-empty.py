"""All-NUL uid and gid fields, as written in most Rust crates.

The archive has a file `a` with GNU magic and 8 NUL bytes in both the uid and gid fields.

In [POSIX][uid-gid], the uid and gid fields store the file's owner and group as [zero-filled octal
numbers][zero-filled]. Ownership is not part of the extracted tree, and some archivers leave both
fields all-NUL instead of writing octal digits. Readers treat the empty fields as 0 or ignore them.

Seen in: 5394 of the scanned tarballs, most of them crates.
"""
F = lambda path, contents: {"path": path, "kind": "file", "contents": contents, "executable": False}

VERDICT = "accept"
ID = "F79"
FEATURES = ["number.uid.no-digits", "number.gid.no-digits"]
TREE = [F("a", b"a\n")]


def build(a):
    a.file(b"a", b"a\n", uid=b"\0", gid=b"\0", magic=b"ustar ", version=b" \0",
           note="all-NUL uid and gid")
    a.end()

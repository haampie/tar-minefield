"""A non-ASCII UTF-8 pax `path`.

The archive has one file with `path=日本語/café.txt` (encoded in UTF-8) in its pax header and
`nihongo/cafe.txt` in its ustar name field.

In [POSIX][utf-8], pax records use UTF-8 and a `path` record [overrides][path] the ustar name and
prefix fields, which is the standard way to store non-ASCII filenames. The extracted file is
`日本語/café.txt`. A reader that decodes the pax record using a different character set, such as
Latin-1, extracts the file under a mangled name.

Seen in: 789 of the scanned tarballs have non-ASCII names, either in a pax `path` or in the ustar
name field.
See also: N03, a long name in a pax `path`, and N18, a non-UTF-8 name.
"""
F = lambda path, contents: {"path": path, "kind": "file", "contents": contents, "executable": False}
D = lambda path: {"path": path, "kind": "directory"}

VERDICT = "accept"
ID = "N54"
FEATURES = ["name.non-ascii"]
TREE = [D("日本語"), F("日本語/café.txt", b"which name?\n")]


def build(a):
    a.pax([(b"path", "日本語/café.txt".encode())], note="non-ASCII UTF-8 path")
    a.file(b"nihongo/cafe.txt", b"which name?\n")
    a.end()

"""A file with a GNU long name and typeflag NUL, whose name field ends in a slash.

The archive has a GNU long name header whose data is 99 `p`s, followed by a slash, followed by
`file.py`, followed by a NUL. After it is a regular file, of typeflag NUL, with GNU's magic. Its
name field contains the first 100 bytes of the long name: the 99 `p`s, followed by the slash.

The long name replaces the name field, so the member is a regular file, `file.py` under the
directory of 99 `p`s, which does not have a member of its own. The long name header is GNU tar's own
format for long names. A name that ends in a slash was the [old way][slash-convention] to archive a
directory. A reader that decides the kind by the name field, before the long name is applied,
extracts a directory instead. A reader that does not apply the long name extracts a file of 99 `p`s,
by the name field without its slash.

Seen in: sdists of Python packages that maturin wrote.
See also: K01, a regular file whose name ends in a slash.
"""
F = lambda path, contents: {"path": path, "kind": "file", "contents": contents, "executable": False}
D = lambda path: {"path": path, "kind": "directory"}

NAME = b"p" * 99 + b"/file.py"

VERDICT = "accept"
ID = "N45"
FEATURES = ["type.nul"]
TREE = [D("p" * 99), F(NAME.decode(), b"print()\n")]
GNU = dict(magic=b"ustar ", version=b" \0")


def build(a):
    a.gnu_long(NAME)
    a.header(NAME[:100], b"\0", 8, note="typeflag NUL, a name field that ends in a slash", **GNU)
    a.data(b"print()\n")
    a.end()

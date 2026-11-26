"""A file with a GNU long name and typeflag NUL, whose name field ends in a slash.

The archive has a GNU long name header (typeflag `L`) containing 99 `p`s, a slash, `file.py`, and a
NUL, followed by a regular file of typeflag NUL with GNU magic. Because the ustar name field holds
the first 100 bytes of the long name, it contains the 99 `p`s followed by `/`.

Applying the GNU long name gives the member its full path (`file.py` inside a directory of 99 `p`s)
as a regular file. However, a trailing slash was the [historical convention][slash-convention] for
directories, and a reader that classifies the member from its 100-byte ustar name field before
applying the long name mistakes the regular file for a directory. A reader that ignores the `L`
header altogether strips the trailing slash from the ustar name field and extracts a regular file
named with 99 `p`s.

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

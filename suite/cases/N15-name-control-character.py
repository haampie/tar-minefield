r"""A control character in a name, here a newline, created as it is.

The archive has one file, `a\nb`, with a newline in its name.

Any byte except `/` and NUL is valid in a Unix filename, including control characters
(`[\x01-\x1f\x7f]`). POSIX [encourages][newline-error] treating a newline in a filename as an error,
yet every reader parses the name identically. The hazard lies in downstream tools: a newline makes
one filename look like two (`a` and `b`) in line-oriented manifests, scripts, or piped `ls` output,
while carriage returns or escape sequences can spoof terminal output. A strict parser may reject
control characters in names; the default policy tolerates them.

Seen in: gocryptfs 2.5.1 and deja-vu 0.4, with newlines, and cdrtools 3.02a09, wgrib2 3.6.0 and
apktool 2.6.0, with ESC and DEL.
"""

F = lambda path, contents: {"path": path, "kind": "file", "contents": contents, "executable": False}

VERDICT = "tolerate"
ID = "N15"
FEATURES = ['name.control-character']
TREE = [F('a\nb', b'a newline in my name\n')]


def build(a):
    a.file(b"a\nb", b"a newline in my name\n")
    a.end()

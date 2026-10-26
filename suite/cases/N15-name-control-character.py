r"""A control character in a name, here a newline, created as it is.

The name `a\nb` is valid on Unix, as is any name with a control character, `[\x01-\x1f\x7f]`, and
every implementation that extracts it creates that name. A tar reader has no other way to read it:
the risk is in what is done with the name afterwards, where a newline makes it look like two names,
`a` and `b`, in the output of `ls` piped to another command, in manifests and in scripts, and a
carriage return or ESC makes a terminal show another name. A strict parser may reject it; the
default policy creates it as it is.

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

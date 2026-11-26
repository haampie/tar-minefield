"""A regular file with a `linkpath` record in its pax header.

The archive has a regular file `a` (typeflag `0`) whose pax header contains `linkpath=target`.

A pax `linkpath` record [overrides][linkpath] the ustar linkname field, which [POSIX][linkname]
defines only for hardlinks and symlinks. Because a member is extracted according to its
[typeflag][file-type], `a` is a regular file. A reader that infers the member kind from the presence
of a link target would create a link to `target` instead. The default policy tolerates it, as the
readers that accept it ignore `linkpath` and extract the same regular file.

Decision point: whether a pax `linkpath` turns a regular file into a link.
Seen in: none of the scanned tarballs.
See also: K02, a regular file with a ustar linkname.
"""

F = lambda path, contents: {"path": path, "kind": "file", "contents": contents, "executable": False}

VERDICT = "tolerate"
ID = "K16"
FEATURES = ["extended.linkpath-on-file"]
TREE = [F("a", b"a file, or a link?\n")]


def build(a):
    a.pax([(b"linkpath", b"target")], note="linkpath on a regular file")
    a.file(b"a", b"a file, or a link?\n")
    a.end()

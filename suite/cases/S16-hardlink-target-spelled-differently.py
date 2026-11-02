"""A hard link to `./a`, where the member is named `a`.

The archive has a file `a`, then a hard link `h` whose target is `./a`.

In POSIX, a hard link represents a file linked to another file [previously archived][hardlink], and
its target is in the [linkname][linkname] field. POSIX does not say whether the target should be
literally the name of an earlier member, or whether it can also be an equivalent path. This case is
ambiguous because `./a` names the file `a`, as a path, or no member, as a name, so that `h` is a
link to `a`, or an error.

Decision point: whether the target of a hard link is a path or the name of a member.
Seen in: none of the scanned tarballs.
See also: S03, a hard link to a member that is not in the archive, and N06, the name `./a`.
"""

F = lambda path, contents: {"path": path, "kind": "file", "contents": contents, "executable": False}

VERDICT = "tolerate"
ID = "S16"
FEATURES = ["hardlink.target-spelled-differently"]
TREE = [F("a", b"a\n"), F("h", b"a\n")]


def build(a):
    a.file(b"a", b"a\n")
    a.hardlink(b"h", b"./a", note="the target spelled ./a")
    a.end()

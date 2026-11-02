"""A hard link to `./a`, where the member is named `a`.

The archive has a file `a`, then a hard link `h` whose target is `./a`.

In POSIX, a hard link represents a file linked to another file [previously archived][hardlink],
and its target is in the [linkname][linkname] field, but POSIX does not say whether the target
must be spelled as that file's name. This case is ambiguous because `./a` names the file `a`, as a
path, or no member, as a name, so that `h` is a link to `a`, or an error.

Decision point: whether the target of a hard link is a path or the name of a member.
Seen in: none of the scanned tarballs.
See also: S03, a hard link to a member that is not in the archive.
"""

VERDICT = "reject"
ID = "S16"
FEATURES = ["hardlink.target-spelled-differently"]


def build(a):
    a.file(b"a", b"a\n")
    a.hardlink(b"h", b"./a", note="the target spelled ./a")
    a.end()

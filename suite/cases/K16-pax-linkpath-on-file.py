"""A regular file with a `linkpath` record in its pax header.

The archive has a regular file `a` (typeflag `0`) whose pax header contains `linkpath=target`.

A pax `linkpath` record [overrides][linkpath] the ustar linkname field, which [POSIX][linkname]
defines only for hardlinks and symlinks. Because a member is extracted according to its
[typeflag][file-type], `a` is a regular file. Most readers either ignore `linkpath` and extract the
file or reject the inconsistent header, but a reader that infers the member kind from the presence
of a link target creates a link to `target` instead.

Decision point: whether a pax `linkpath` turns a regular file into a link.
Seen in: none of the scanned tarballs.
See also: K02, a regular file with a ustar linkname.
"""

VERDICT = "reject"
ID = "K16"
FEATURES = ["extended.linkpath-on-file"]


def build(a):
    a.pax([(b"linkpath", b"target")], note="linkpath on a regular file")
    a.file(b"a", b"a file, or a link?\n")
    a.end()

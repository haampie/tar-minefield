r"""Bytes after the NUL that ends the target of a symlink.

The archive has one symlink, `l`, whose linkname field contains `safe`, followed by a NUL, followed
by `../x`.

In [POSIX][name-full], the linkname field is a string that ends with a NUL, except when it fills the
field, so the target is `safe`. Copied as a whole, the field is `safe` as a C string, which ends at
the first NUL, but `safe\0../x` in languages whose strings can contain a NUL: creating the link then
fails, or the string that is checked is not the one that is used.

The bytes after the NUL do not mean anything, and writers do not put them there, so a strict parser
rejects them rather than guess what they are for.

Decision point: where a link target ends.
Seen in: none of the scanned tarballs.
See also: N14, bytes after the NUL that ends a name.
"""

VERDICT = "reject"
ID = "N51"
FEATURES = ["linkname.bytes-after-nul"]


def build(a):
    a.symlink(b"l", b"safe\0../x", note="bytes after the NUL of its target")
    a.end()

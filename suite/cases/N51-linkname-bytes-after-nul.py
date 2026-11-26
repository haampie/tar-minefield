r"""Trailing bytes after the NUL terminator in a symlink target.

The archive has a symlink `l` whose linkname field contains `safe`, a NUL byte, and `../x`.

Under [POSIX][name-full], the linkname field is NUL-terminated unless it fills all 100 bytes, so the
link target is `safe`. A reader that copies the whole field instead of stopping at the first NUL
sees `safe\0../x` in languages with length-delimited strings, whereas C system calls stop at the
NUL. Creating the symlink then fails, or the string that is checked is not the one that is used.

Because normal archivers zero-fill the remainder of the field and trailing bytes after the NUL have
no valid purpose, a strict parser rejects the archive.

Decision point: whether a linkname ends at its first NUL.
Seen in: none of the scanned tarballs.
See also: N14, trailing bytes after the NUL in a name.
"""

VERDICT = "reject"
ID = "N51"
FEATURES = ["linkname.bytes-after-nul"]


def build(a):
    a.symlink(b"l", b"safe\0../x", note="bytes after the NUL in linkname")
    a.end()

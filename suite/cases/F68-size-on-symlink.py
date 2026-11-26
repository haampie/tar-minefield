"""A non-zero size in a symlink header, covering the next member's header.

The archive has a symlink `l` to `target` with a size field of 512, followed by an empty file
`smuggled` and a file `b`.

Under [POSIX][no-data], symlinks do not store data blocks and their size field [must be
zero][link-size-zero], so the following block is `smuggled`'s header. A reader that ignores the size
field extracts `l`, `smuggled` and `b`, whereas one that skips 512 bytes of data misses `smuggled`
and extracts only `l` and `b`. Some readers take the 512-byte block as the link target, creating a
symlink to `smuggled` from the name at the start of that header; others extract `l` as a regular
file containing the block, or reject the archive.

Decision point: whether a non-zero size in a symlink header consumes data blocks.
Seen in: none of the scanned tarballs.
See also: F46, a pax `size` on a symlink, and F34, a non-zero size on a hardlink.
"""

VERDICT = "reject"
ID = "F68"
FEATURES = ["size.on-symlink"]


def build(a):
    a.header(b"l", b"2", 512, linkname=b"target", note="symlink with size 512")
    a.file(b"smuggled", b"", note="covered by l's size")
    a.file(b"b", b"b\n")
    a.end()

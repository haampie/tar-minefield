"""A hardlink with mode 755 to a file with mode 644.

The archive has a file `a` with mode 644, followed by a hardlink `h` to `a` with mode 755.

A [hardlink][hardlink] is a second directory entry for an existing file, and all hardlinks to one
inode share a single mode. Archivers normally record the same mode in both headers, whereas here the
modes disagree. A reader that ignores the hardlink's mode leaves the shared file at mode 644
(non-executable under both names). A reader that applies the hardlink's mode changes the shared file
to 755 (executable under both names). Finally, a reader that copies the target instead of
hardlinking it leaves `a` non-executable and makes `h` executable.

Decision point: whether a hardlink header's mode updates the linked file's mode.
Seen in: not measured, as the scanner does not record modes; 233 scanned tarballs contain hardlinks.
See also: S17, a file followed by a hardlink and a second copy of the file, and K09, an executable
file.
"""

VERDICT = "reject"
ID = "S29"
FEATURES = ["hardlink.mode-differs"]


def build(a):
    a.file(b"a", b"a\n")
    a.hardlink(b"h", b"a", mode=0o755, note="mode 755 (target a has 644)")
    a.end()

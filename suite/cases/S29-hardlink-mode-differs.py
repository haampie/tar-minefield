"""A hardlink with the mode 755, to a file with the mode 644.

The archive has a file `a` with the mode 644, then a hardlink `h` to `a` whose header has the mode
755.

A [hardlink][hardlink] is a second name for a file archived before it, and a file has one mode,
whatever its names. Writers write the mode of the file in both headers, so that the two are the
same; here they differ. This case is ambiguous because a reader can take the mode of the link in one
of three ways. A reader that does not apply it extracts a file that is not executable, under both
names. One that applies the mode of every header extracts an executable file, under both names. One
that copies the file, where others link, extracts `h` as an executable file, and `a` as one that is
not.

Decision point: whether the mode in the header of a hardlink applies to the file.
Seen in: not measured, as the scans do not record modes: 233 of the scanned tarballs have hardlinks.
See also: S17, a file, a hardlink to it, then the file again, and K09, an executable file.
"""

VERDICT = "reject"
ID = "S29"
FEATURES = ["hardlink.mode-differs"]


def build(a):
    a.file(b"a", b"a\n")
    a.hardlink(b"h", b"a", mode=0o755, note="mode 755, where a has 644")
    a.end()

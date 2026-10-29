"""No end-of-archive marker: the archive ends after a complete member.

The archive has a file `a`, and ends right after its data, without zero blocks.

[POSIX][end] requires two zero blocks at the end of an archive. Without them, an archive cannot be
told apart from one cut short after a member, but the implementations that extract it all extract
the same tree, and ruby's release tarballs are written this way. The default policy extracts it: a
compressed archive that is cut short is caught by its decompression.

Decision point: whether an archive without an end-of-archive marker is complete.
Seen in: SDL2_image 2.8.8, ruby 4.0.5 and fastcap 2.0-18Sep92.
See also: F08, an archive cut short inside the data of a member, which is rejected.
"""

F = lambda path, contents: {"path": path, "kind": "file", "contents": contents, "executable": False}

VERDICT = "tolerate"
ID = "F04"
FEATURES = ['end.missing']
TREE = [F('a', b'a\n')]


def build(a):
    a.file(b"a", b"a\n")

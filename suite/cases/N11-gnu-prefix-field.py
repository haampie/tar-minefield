"""The prefix field of a header with GNU magic, which GNU tar uses for times in incremental archives.

The archive has one file, `a`, with GNU magic and two timestamps, `15000000000` and `15000000000`,
at the offset of ustar's prefix field.

GNU's format does not have a prefix field; in incremental archives, GNU tar stores access and change
times at that offset. A reader that treats those bytes as a ustar prefix extracts `a` inside a
directory named `15000000000`.

Decision point: whether a header with GNU magic has a prefix.
Seen in: none of the scanned tarballs with times there.
"""

VERDICT = "reject"
ID = "N11"
FEATURES = ['gnu.atime-ctime']


def build(a):
    a.file(b"a", b"a\n", magic=b"ustar ", version=b" \0", prefix=b"15000000000\0" + b"15000000000\0",
           note="GNU magic, with an access and change time where ustar has its prefix")
    a.end()

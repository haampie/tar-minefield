"""The prefix field of a header with GNU magic, which GNU tar uses for times in incremental archives.

GNU's format has no prefix field: in incremental archives, GNU tar writes the access and change
times where ustar has its prefix. This case is ambiguous in practice because the field, taken for
ustar's prefix, puts `a` under a directory `15000000000`, which Python's `tarfile` does (gh-155629).

Decision point: whether a header with GNU magic has a prefix.
Seen in: no source tarball with times there.
"""

VERDICT = "reject"
ID = "N11"
FEATURES = ['gnu.atime-ctime']


def build(a):
    a.file(b"a", b"a\n", magic=b"ustar ", version=b" \0", prefix=b"15000000000\0" + b"15000000000\0",
           note="GNU magic, with an access and change time where ustar has its prefix")
    a.end()

r"""A prefix in a header with GNU's magic and the version `"00"`: part of the name, or not?

The archive has one file, whose header has GNU's magic, `"ustar "`, the version `"00"`, the name
`a` and the prefix `p`.

The ustar format defines the pathname as the [prefix][prefix], followed by `/`, followed by the
name. GNU's format has a very similar magic, but no prefix field: in GNU's own definition, its magic
is the 8 bytes `"ustar  \0"`, in place of ustar's magic and version. This case is ambiguous because
the 8 bytes of this header, `"ustar 00"`, are of neither format: a reader that checks the magic
before the prefix extracts `a`, as a GNU or a v7 header, and one that reads the prefix regardless
extracts `p/a`.

Decision point: which magic and version make the prefix part of the name.
Seen in: none of the scanned tarballs.
See also: N04, a name split by the ustar prefix, and N11, a GNU header with times where ustar has
its prefix.
"""

VERDICT = "reject"
ID = "F47"
FEATURES = ["magic.other"]


def build(a):
    a.file(b"a", b"a\n", magic=b"ustar ", version=b"00", prefix=b"p",
           note="GNU's magic, the version of POSIX, and a prefix")
    a.end()

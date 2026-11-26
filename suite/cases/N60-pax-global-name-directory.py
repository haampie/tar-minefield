"""A global pax header whose ustar name contains a directory component.

The archive has a global pax header named `g/pax_global_header` with a `comment` record, followed by
a file `a`.

A [global pax header][global-files] is metadata, not an archive member, and a pax-aware reader
ignores its ustar name field. Archivers routinely include a directory in that field: [by
default][globexthdr-name], POSIX names global headers `$TMPDIR/GlobalHead.%p.%n` and extended
headers `%d/PaxHeaders.%p/%f`. The extracted tree is therefore just `a`. A reader that creates
parent directories for a header's ustar name before checking its typeflag leaves behind an empty
directory `g`.

Seen in: gpa 0.11.0 and 0.11.1 and drbd 9.3.3, whose global headers GNU tar named
`/tmp/GlobalHead.1`.
See also: F17, the global header written by `git archive`, and N52, a pax header named with `..`.
"""
F = lambda path, contents: {"path": path, "kind": "file", "contents": contents, "executable": False}

VERDICT = "accept"
ID = "N60"
FEATURES = []
TREE = [F("a", b"a\n")]


def build(a):
    a.pax([(b"comment", b"a global header")], typeflag=b"g", name=b"g/pax_global_header",
          note="ustar name in a subdirectory")
    a.file(b"a", b"a\n")
    a.end()

"""A global pax header whose own name has a directory.

The archive has a global header that is itself named `g/pax_global_header`, with a `comment` record,
then a file `a`.

The name of a [global header][global-files] is not the name of a member, and a reader of pax does
not use it. So the tree is the file `a`, without a directory `g`. A reader that creates the parent
directories of every header, before it looks at its typeflag, leaves an empty directory `g`. A name
in a directory is what a writer gives these headers: [by default][globexthdr-name], a global header
is named `$TMPDIR/GlobalHead.%p.%n`, with the process ID and a sequence number, and an extended
header `%d/PaxHeaders.%p/%f`, with the directory and the name of its member.

Seen in: gpa 0.11.0 and 0.11.1 and drbd 9.3.3, whose global headers GNU tar named
`/tmp/GlobalHead.1`.
See also: F17, the global header that `git archive` writes, and N52, a pax header whose name has
`..`.
"""
F = lambda path, contents: {"path": path, "kind": "file", "contents": contents, "executable": False}

VERDICT = "accept"
ID = "N60"
FEATURES = []
TREE = [F("a", b"a\n")]


def build(a):
    a.pax([(b"comment", b"a global header")], typeflag=b"g", name=b"g/pax_global_header",
          note="named in a directory")
    a.file(b"a", b"a\n")
    a.end()

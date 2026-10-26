"""The global pax header with only a `comment`, as `git archive` writes it.

A tarball created with `git archive` from a commit or a tag starts with a global header whose only
record is the commit, as a `comment`, which does not affect extraction. GitHub's release tarballs
are made this way, so a strict parser that rejects global headers rejects most of them.

Seen in: tarballs created with `git archive`, such as GitHub's release tarballs.
"""

VERDICT = "accept"
ID = "F17"
TREE = [
    {"path": "project", "kind": "directory"},
    {"path": "project/README", "kind": "file", "contents": b"hello\n", "executable": False},
]


def build(a):
    a.pax(
        [(b"comment", b"0123456789abcdef0123456789abcdef01234567")],
        typeflag=b"g",
        name=b"pax_global_header",
        note="the commit, as git archive writes it",
    )
    a.directory(b"project/", mode=0o775)
    a.file(b"project/README", b"hello\n", mode=0o664)
    a.end()

"""pax `atime` and `ctime` records, as GNU tar's posix format writes them.

GNU tar with `--format=posix`, bsdtar and star write the access and change times of every member
as pax records, next to its `mtime`. `ctime` is no longer a keyword of POSIX, and keywords of
lowercase letters, digits and periods are reserved, so a strict parser that rejects unknown or
reserved keys rejects these tarballs. Neither key affects the tree.

Seen in: hundreds of the scanned tarballs, such as gcc 15.2.0 and avahi 0.8.
"""

VERDICT = "accept"
ID = "F37"
TREE = [
    {"path": "file", "kind": "file", "contents": b"hello\n", "executable": False},
]


def build(a):
    a.pax(
        [
            (b"mtime", b"1700000000.123456789"),
            (b"atime", b"1700000001.5"),
            (b"ctime", b"1700000000.123456789"),
        ],
        name=b"PaxHeaders/file",
        note="the times, as GNU tar writes them",
    )
    a.file(b"file", b"hello\n")
    a.end()

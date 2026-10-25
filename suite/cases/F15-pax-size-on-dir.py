"""A pax `size` on a directory, which takes the next header for its data.

The pax extended header of a directory has `size=512`. In POSIX, no data is stored for a directory,
whatever its size, so the next block is the header of a file, `smuggled`. This case is ambiguous in
practice because, if the size applies, that block is the directory's data instead, and the tree is a
directory alone. This is the bug class of CVE-2025-62518 (tokio-tar), GHSA-3pv8-6f4r-ffg2 (tar-rs)
and CVE-2026-53655 (node-tar), where the hidden block is a header that only one implementation sees.

Decision point: whether a pax `size` applies to a member that has no data.
Seen in: llama_index_workflows 2.26.0, with a pax size on a directory.
See also: F33, a size in the ustar header of a directory, which is rejected as well.
"""

VERDICT = "reject"
ID = "F15"
FEATURES = ["pax.size-on-dir"]
POSIX = "no-data"


def build(a):
    a.pax([(b"size", b"512")], note="for dir/, with size=512")
    a.directory(b"dir/", note="no data, but the pax size is 512")
    a.file(b"dir/smuggled", b"", note="the block that the pax size covers")
    a.end()

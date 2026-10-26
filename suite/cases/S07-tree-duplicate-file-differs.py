"""The same file twice, with different contents: the first copy, or the last?

The archive has two members named `a`, with different contents. This case is ambiguous because
either copy can be the file, and the two trees differ in the contents of `a`: every implementation
that extracts it keeps the last copy, but an extractor that does not overwrite files, such as GNU
tar with `--keep-old-files`, keeps the first.

Decision point: which of two members of one path is the file.
Seen in: fish 4.7.1, where `Cargo.toml` and `Cargo.lock` are appended again without their last
newline, and logstash 8.15.2, where `build.rb` is first a license header and last the build's
date and commit. Most tarballs with duplicates, mostly from `cabal sdist`, have identical copies:
the default policy rejects those too, as an implementation would have to compare the copies to tell.
"""

VERDICT = "reject"
ID = "S07"
FEATURES = ["tree.duplicate.file-file"]


def build(a):
    a.file(b"a", b"first\n", note="the first copy")
    a.file(b"a", b"last\n", note="the last copy")
    a.end()

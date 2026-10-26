# Scan of all 37757 Spack tarballs, 2026-10-23

Every tarball of Spack's builtin repository on Linux x86_64, not a sample, in the order of
`run.py fraction`, so that any prefix of `sample.jsonl` is a uniform sample:

```console
$ python -I scanner/run.py fraction ../lists/73b099d5c1-linux-x86_64.jsonl 1 0 > sample.jsonl
$ TMPDIR=/tmp python -I scanner/run.py scan sample.jsonl results.jsonl --untar ~/untar --jobs 16 \
      --reuse ../../nix/2026-10-23/results.jsonl --reuse ../../guix/2026-10-23/results.jsonl \
      --reuse ../../live-bootstrap/2026-10-23/results.jsonl
$ python -I scanner/report.py --title "Scan of all 37757 Spack tarballs" results.jsonl > REPORT.md
```

- Scanner: `tarscan.py` version `25bfa32e6e71`.
- Packages: spack-packages `73b099d5c1118951de3ac69b91e6f73afc41690e` (2026-10-19), listed with
  Spack `37c7f2646acbdf12bd3fae177e1daff3f2d7ce0b` on Linux x86_64: see
  [../lists/README.md](../lists/README.md). The list has an entry per version, so a tarball that
  several versions share is listed more than once: `sample.jsonl` has each once.
- untar: `2305390138cf436059b89b7b15146dc5213a3ba5`, `untar.py` version `51a9c3aa565c`.
- Platform: Ubuntu 26.04 (Linux 7.0) on x86_64, Python 3.14.4. untar extracted to tmpfs, and to
  ext4 for some tarballs that did not fit: both are case-sensitive, so no failures are caused by
  the filesystem.

This replaces two samples of about 2000 tarballs each, scanned on macOS, whose filesystem is
case-insensitive. They are in the history of this repository, at `data/spack/2026-10-23` and
`data/spack/2026-10-23-b` before this scan took their place.

The scan ran with 8 jobs, then 16, and was interrupted and run again: `run.py scan` continues
where it stopped. It first reused the results of the two macOS samples. Three passes then
completed it, each after removing from `results.jsonl` the rows it redoes:

- the rows copied from the macOS samples, scanned again on Linux, and the tarballs that untar
  skipped because tmpfs (16 GB) was full, extracted again with 6 jobs, to tmpfs;
- the tarballs that could not be downloaded, tried again.

nvhpc, whose 39 tarballs are 10 GB each, was left out of the second pass: 34 of them keep their
rows with `untar_skipped`, and 5 were extracted on disk, one at a time. Of the other tarballs,
those that still did not fit in the second pass keep `untar_skipped`, mostly CUDA, ROCm and
compiler binaries. Their headers are scanned in full, so every strict criterion is assessed for
them: only whether untar extracts them is not. REPORT.md lists them.

Downloads: mirror.spack.io first, then the upstream URL. REPORT.md counts the downloads by host.
Every tarball that could not be downloaded failed with 404 on the mirror, and upstream mostly
with 404 too, or with a file of a different sha256.

One file is no tar archive: py-multiprocess 0.70.12.2, `multiprocess-0.70.12.2.tar.gz` from PyPI,
is a zip (it starts with `PK\3\4`), which `tarscan.py` stops at with `invalid checksum at offset
0`. `strict.py` does not assess a file that it cannot read the first header of, so it is not
counted as rejected.

## Scanned again, 2026-10-24

`tarscan.py` `5b9b83abac66` reports features that `25bfa32e6e71` did not, for the cases F20 to F31
and N22 to N24. `UNREPORTED` in `contrib/scanner/strict.py` lists them, and rules them out from
what `25bfa32e6e71` recorded in most tarballs. The 44 tarballs of this scan where it rules out
neither a strict criterion nor a binary value of a vendor pax key were scanned again, with the
same untar, and their rows in `results.jsonl` replaced:

```console
$ python -I contrib/scanner/run.py scan sample-spack.jsonl results-spack.jsonl --untar ~/untar --jobs 8
```

where `sample-spack.jsonl` has the lines of `sample.jsonl` for those tarballs: those for which
`strict.unmeasured_criteria(r)` is not empty, or `strict.unmeasured(r)` has a
`pax.value-not-utf8.*` feature of a key other than `mtime`, `atime`, `ctime`, `uid` and `gid`.
Every row is as it was, but for the new features: 11 tarballs have
`pax.value-not-utf8.SCHILY.xattr.*`, which is allowed. The other rows keep `25bfa32e6e71`.

# Scan of all 10200 Guix tarballs, 2026-10-23

Every tarball of the current revision of Guix, not a sample, from the list of sources that Guix
publishes for Software Heritage:

```console
$ curl -o sources.json https://guix.gnu.org/sources.json
$ python -I scanner/guix_list.py sources.json > sample.jsonl
$ TMPDIR=/tmp python -I scanner/run.py scan sample.jsonl results.jsonl \
      --untar ~/untar --jobs 8 --cache ~/.cache/tar-minefield \
      --reuse ../../nix/2026-10-23/results.jsonl --reuse ../../live-bootstrap/2026-10-23/results.jsonl
$ python -I scanner/report.py --title "Scan of all 10200 Guix tarballs" results.jsonl > REPORT.md
```

- Scanner: `tarscan.py` version `25bfa32e6e71`.
- Packages: Guix `37bb0f08195f8fd09a6c75bff9f07940d817605c`, the revision in `sources.json`,
  downloaded on 2026-10-23. Of its sources, those fetched by URL with a sha256 whose name is
  that of a tarball: 10,200 distinct tarballs of 9,706 packages, 2,474 of them also in the Nix
  scan. Like nixpkgs, one revision has about one version of each package; `latest` is the
  highest version of a package, by the name of its tarball.
- untar: `2305390138cf436059b89b7b15146dc5213a3ba5`, `untar.py` version `51a9c3aa565c`.
- Platform: Ubuntu 26.04 (Linux 7.0) on x86_64, Python 3.14.4. untar extracted to ext4 for the
  first part of the scan, then to tmpfs, which was faster: both are case-sensitive, so no failures
  are caused by the filesystem.

The numbers above are from `sample.jsonl` and the Nix scan:

```console
$ python3 -I -c '
import json
g = [json.loads(l) for l in open("data/guix/2026-10-23/sample.jsonl")]
n = {json.loads(l)["sha256"] for l in open("data/nix/2026-10-23/sample.jsonl")}
print(len(g), len({t["package"] for t in g}), sum(t["sha256"] in n for t in g))'
10200 9706 2474
```

The scan was interrupted and run again several times, which `run.py scan` continues where it
stopped. Three passes then completed it, each after removing the rows it redoes from
`results.jsonl`, and with `TMPDIR=~/.cache/tar-minefield-tmp` on ext4:

- the tarballs that untar skipped because tmpfs (16 GB) was full, mostly large ones such as
  rustc, firefox and chromium, extracted while other workers filled it;
- the rows copied from two samples of Spack, scanned on macOS, whose filesystem is
  case-insensitive, and which are no longer in this repository: scanned again on Linux, with
  `--reuse` of the Nix scan, their features and untar's results were the same;
- the tarballs that could not be downloaded, nearly all because bordeaux.guix.gnu.org answered
  with 502 for a while.

Downloads: `guix_list.py` puts Guix's own content-addressed mirrors first, bordeaux.guix.gnu.org
and ci.guix.gnu.org, then tarballs.nixos.org, then at most three upstream URLs. REPORT.md counts
the downloads by host. The one tarball that could not be downloaded, dovecot-trees 2.1.0, fails
with 404 on every URL.

Like Nix, Guix has some `.tar.lz` and `.tar.zst` tarballs, which `tarscan.py` does not
decompress: it stops at the first header (`invalid checksum at offset 0`), and untar rejects
them. REPORT.md lists them among the tarballs where the scanner stopped early; `strict.py` counts
them as not assessed.

## Scanned again, 2026-10-24

`tarscan.py` `5b9b83abac66` reports features that `25bfa32e6e71` did not, for the cases F21, F26,
F27, F30, F31, N22 and N23. `UNREPORTED` in `contrib/scanner/strict.py` lists them, and rules them out from
what `25bfa32e6e71` recorded in most tarballs. The 10 tarballs of this scan where it rules out
neither a strict criterion nor a binary value of a vendor pax key were scanned again, with the
same untar, and their rows in `results.jsonl` replaced:

```console
$ python -I contrib/scanner/run.py scan sample-guix.jsonl results-guix.jsonl --untar ~/untar --jobs 8 --reuse results-spack.jsonl --reuse results-nix.jsonl
```

where `sample-guix.jsonl` has the lines of `sample.jsonl` for those tarballs: those for which
`strict.unmeasured_criteria(r)` is not empty, or `strict.unmeasured(r)` has a
`pax.value-not-utf8.*` feature of a key other than `mtime`, `atime`, `ctime`, `uid` and `gid`.
Every row is as it was, but for the new features: 6 tarballs have
`pax.value-not-utf8.SCHILY.xattr.*`, which is allowed. The other rows keep `25bfa32e6e71`.

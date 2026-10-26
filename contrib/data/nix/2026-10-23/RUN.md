# Scan of all 19086 nixpkgs tarballs, 2026-10-23

Every tarball that the Hydra jobs of nixpkgs fetch with `fetchurl`, not a sample. In a checkout
of nixpkgs, with the jobs of `all-tarballs.nix` evaluated in chunks of 1000, each in its own
process (all at once takes over 10 GB of memory):

```console
$ nix-instantiate --eval --json --strict -E \
      'builtins.attrNames (import ./maintainers/scripts/all-tarballs.nix)' > attrs.json
$ # for each chunk.json of 1000 names of attrs.json:
$ nix-instantiate --readonly-mode --eval --json --strict maintainers/scripts/find-tarballs.nix \
      --arg expr 'let all = import ./maintainers/scripts/all-tarballs.nix;
                  in map (n: all.${n}) (builtins.fromJSON (builtins.readFile ./chunk.json))' \
      > chunk-files.json
$ nix-instantiate --eval --json --strict -E \
      'removeAttrs (import ./pkgs/build-support/fetchurl/mirrors.nix) [ "hashedMirrors" ]' \
      > mirrors.json
$ python -I scanner/nix_list.py mirrors.json chunk-*-files.json > sample.jsonl
$ TMPDIR=~/.cache/tar-minefield-tmp python -I scanner/run.py scan sample.jsonl results.jsonl \
      --untar ~/untar --jobs 8 --cache ~/.cache/tar-minefield \
      --reuse ../../guix/2026-10-23/results.jsonl --reuse ../../live-bootstrap/2026-10-23/results.jsonl
$ python -I scanner/report.py --title "Scan of all 19086 nixpkgs tarballs" results.jsonl > REPORT.md
```

The scan started on the chunks that were evaluated, and was run again as more were: `run.py
scan` skips the tarballs it has. It first reused the results of two samples of Spack, scanned on
macOS, which are no longer in this repository. Their 210 rows were removed from `results.jsonl`
and scanned again on Linux, with `--reuse` of the Guix scan, which copied 2 of them; the features
and untar's results of all 210 were the same as on macOS.

- Scanner: `tarscan.py` version `25bfa32e6e71`.
- Packages: nixpkgs `75ba83324cc35b3e156ac46ee379f38e8f0b1808` (2026-10-23), 25,703 jobs for
  x86_64-linux. Evaluated with the static Nix 2.28.9 of Hydra build 349255020 (sha256
  `7f1eded4292ff1159ef938b134d7016d09b6d678325d638ac82eb4a93466d150`), without a daemon and
  with `--readonly-mode`: 26 chunks, 13 minutes in total, at most 10.6 GB of memory for a chunk.
- untar: `2305390138cf436059b89b7b15146dc5213a3ba5`, `untar.py` version `51a9c3aa565c`.
- Platform: Ubuntu 26.04 (Linux 7.0) on x86_64, Python 3.14.4. untar extracted to ext4, which is
  case-sensitive, so no failures are caused by the filesystem.

What the list holds: the files that nixpkgs fetches with a flat hash, so not those of
`fetchFromGitHub` or `fetchzip`, which hash the unpacked tree, and of those, the tar files with a
sha256 that are not changed after the download. One revision of nixpkgs has about one version
of each package, so nearly all are `latest`: 1,035 are not, mostly where nixpkgs has several
versions of a package (`latest` is the highest). It has whole package ecosystems, abandoned
packages included: 7,190 tarballs (38%) are from Hackage, 3,851 from PyPI and 1,899 from CPAN.
Read results by origin, so that one producer, such as `cabal sdist`, does not dominate.

Downloads: tarballs.nixos.org first, then the upstream URLs, which nixpkgs lists after it: the
mirror does not have about half of them, Hackage's above all. REPORT.md counts the downloads by
host, and those that could not be downloaded from any URL: on tarballs.nixos.org, which they
are all tried on first, they failed with 404, so they are not transient errors of the mirror.
Their upstream URLs mostly fail with 404 too, and some serve a file with a different sha256. The
first run took 35 minutes.

22 tarballs are `.tar.lz` (11) and `.tar.zst` (11), which `tarscan.py` does not decompress. It
scans them as uncompressed, stops at the first header (`invalid checksum at offset 0`), and untar
rejects them with `Archive contains an invalid number`. These are not rejections of the
archives: of the 100 that untar rejects, 78 are.

## Scanned again, 2026-10-24

`tarscan.py` `5b9b83abac66` reports features that `25bfa32e6e71` did not, for the cases F21, F26,
F27, F30, F31, N22 and N23. `UNREPORTED` in `contrib/scanner/strict.py` lists them, and rules them out from
what `25bfa32e6e71` recorded in most tarballs. The 27 tarballs of this scan where it rules out
neither a strict criterion nor a binary value of a vendor pax key were scanned again, with the
same untar, and their rows in `results.jsonl` replaced:

```console
$ python -I contrib/scanner/run.py scan sample-nix.jsonl results-nix.jsonl --untar ~/untar --jobs 8 --reuse results-spack.jsonl
```

where `sample-nix.jsonl` has the lines of `sample.jsonl` for those tarballs: those for which
`strict.unmeasured_criteria(r)` is not empty, or `strict.unmeasured(r)` has a
`pax.value-not-utf8.*` feature of a key other than `mtime`, `atime`, `ctime`, `uid` and `gid`.
Every row is as it was, but for the new features: 16 tarballs have
`pax.value-not-utf8.SCHILY.xattr.*`, which is allowed. The other rows keep `25bfa32e6e71`.

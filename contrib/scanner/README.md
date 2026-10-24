# Scanning real tarballs

These scripts measure which tar features real release tarballs use, so that the rules of a
strict parser can be checked against them before anyone adopts them (see
[METHOD.md](../../METHOD.md)). They use the Python standard library only, and Python 3.8 or later.

- `tarscan.py` reads the headers of an archive, skips its data, and reports every feature it
  finds, without stopping at the first one. It is independent of any tar implementation.
- `run.py sample` picks a sample from a list of tarballs, and `run.py scan` downloads and scans
  it. Tarballs are streamed: they are not written to disk, unless they are cached.
- `report.py` summarizes results as Markdown.
- `spack_list.py`, `nix_list.py`, `guix_list.py` and `live_bootstrap_list.py` list the tarballs
  of Spack's builtin repository, nixpkgs, Guix and live-bootstrap. `pypi_list.py`, `crates_list.py`
  and `rubygems_list.py` list the sdists, crates and gems of as many PyPI projects, crates and gems
  as a sample of them needs. Lists for other ecosystems go next to them,
  as `<ecosystem>_list.py`.

Run the scripts with `python -I`: they handle untrusted data, and should not import modules from
the current directory.

## Workflow

```console
$ python -I contrib/scanner/run.py sample list.jsonl 2000 0 > sample.jsonl
$ python -I contrib/scanner/run.py scan sample.jsonl results.jsonl --untar ~/untar --jobs 8 \
      --reuse contrib/data/spack/2026-10-23/results.jsonl
$ python -I contrib/scanner/report.py --title "Scan of 2000 tarballs" results.jsonl > REPORT.md
```

An interrupted `scan` continues where it stopped when run again with the same output. So does a
second pass: remove the rows to redo from the output, such as those with `untar_skipped`
because untar ran out of space (where `TMPDIR` is a small tmpfs, say), and run it again with
more space. `--reuse` does not copy rows with `untar_skipped`.

`--untar PATH` also extracts every tarball with [untar](https://github.com/haampie/untar) from
the checkout at PATH, in a child process that reads from a pipe. Leave it out to scan only.

`--reuse FILE` copies results for tarballs (by sha256) that FILE has from the same versions of
the scanner and untar, instead of downloading them again. Pass the results of every ecosystem
scanned so far: ecosystems share many tarballs, GNU releases above all. Each ecosystem is still
sampled in full, so its fractions are unbiased.

`--cache DIR` also keeps downloaded tarballs in DIR, by sha256, up to `--cache-size GB` (50 by
default), and scans them from there in later runs: a new version of the scanner or untar then
needs no downloads. The least recently used tarballs are removed first, but never those the
current run used: runs read tarballs in the same order, so plain LRU would remove each one just
before it is needed. Tarballs over a tenth of the size are not kept. Workers share DIR without
locks, and so can several runs. The files in it are compressed tarballs with their URL on the
first line, and are never extracted there.

## Lists

A list has one JSON object per line, for one tarball:

| field | |
|---|---|
| `package`, `version` | required |
| `sha256` | required, in hex: downloads are checked against it |
| `url` | required: where the tarball comes from, used to group results by origin |
| `urls` | optional: where to download it, in order. Put a content-addressed mirror first, and `url` last |
| `latest` | optional: whether this is the latest version of the package |

Other fields are kept as they are. Only list tarballs that anyone can download: skip packages
that need a manual download or a license. Tarballs that cannot be downloaded from any of their
URLs are recorded with a `download_error`, and otherwise ignored: many old ones are only on ftp
servers that are gone.

Content-addressed mirrors that serve tarballs by sha256:

- Spack: `https://mirror.spack.io/_source-cache/archive/<sha256[:2]>/<sha256>.<ext>`
- Nix: `https://tarballs.nixos.org/sha256/<sha256>` (hex works, and redirects), which has about
  half of them. `nix_list.py` says how to list them: see `contrib/data/nix/2026-10-23/RUN.md`.
- Guix: `https://bordeaux.guix.gnu.org/file/<name>/sha256/<nix-base32>`, which
  `https://guix.gnu.org/sources.json` lists among the URLs of each source; it only has the
  current revision of Guix. `guix_list.py` makes a list of it.

Other sources worth scanning:

- [live-bootstrap](https://github.com/fosslinux/live-bootstrap): the old tarballs needed to
  bootstrap a GNU/Linux system from source, so a likely place for historical edge cases. Each
  `steps/<step>/sources` has lines `f <url> <sha256> [<name>]`, and `g <repo>~<ref> <url> <sha256>
  [<name>]` for tarballs of git references. There are under 200, so scan all of them rather than
  a sample. Its mirrors (`live-bootstrap.stikonas.eu`, `samuelt.me/pub/live-bootstrap`) serve
  every file by name, also those it makes with `git archive`, and are much faster than the GNU
  upstreams. Two are `.tar.lzma`, which `tarscan.py` does not detect: see
  `contrib/data/live-bootstrap/2026-10-23/RUN.md`.

The sampler takes half latest versions of distinct packages and half older versions of other
packages. Without `latest`, every tarball counts as older. Its order depends only on the seed and
the names of packages and checksums of tarballs, so the sample of a slightly different list is
mostly the same. `run.py fraction LIST P SEED` instead takes about a fraction P of the tarballs,
each by its sha256 alone: a list can be sampled while it is made, and a larger P only adds
tarballs.

## Results

`run.py scan` writes the fields of the list entry, plus:

| field | |
|---|---|
| `scanner`, `untar` | versions: the first 12 hex digits of the sha256 of `tarscan.py` and `untar.py` |
| `source` | the URL it was downloaded from |
| `reused` | true if its results were copied from another results file, with `--reuse` |
| `cached` | true if it was read from `--cache`: `source` is where it was downloaded from before |
| `bytes` | the size of the tarball |
| `members`, `kinds` | number of members, by kind |
| `features` | how often each feature occurs: the names are defined in `tarscan.py` |
| `examples` | up to 3 member names per feature |
| `fingerprint` | how fields are written, to identify the program that wrote the tarball |
| `mtime` | the smallest, median and largest mtime of members, which dates the tarball |
| `compression` | the format, number of streams, and bytes after the last one |
| `error` | why the scanner stopped early, if it did: features before that point are counted |
| `untar_error` | untar's error, or null if it extracted the tarball |
| `untar_skipped` | why untar did not finish, where that says nothing about the tarball (no disk space) |
| `download_error` | instead of all of the above, if no URL worked |

Features under `platform.*` are names that some filesystems cannot hold: they are not ambiguous,
and untar failing on them depends on the machine (see METHOD.md). The report counts failures
caused only by the case-insensitive filesystem of the scanning machine apart from rejections, so
say which filesystem a scan ran on.

## Data

Each scan goes in `contrib/data/<ecosystem>/<date>/`, with:

- `sample.jsonl`: the sample, so the scan can be repeated,
- `results.jsonl`: the output of `run.py scan`,
- `REPORT.md`: the output of `report.py`,
- `RUN.md`: the commands, the commits of this repository, of the ecosystem's package
  repository and of untar, and the platform and filesystem the scan ran on.

`contrib/data/REPORT.md` combines all scans, `contrib/data/STRICT.md` gives what a strict parser
rejects, and the summary of those in the top-level README is generated too:

```console
$ python -I contrib/scanner/report.py --title "All scans" contrib/data/*/*/results.jsonl \
      > contrib/data/REPORT.md
$ python -I contrib/scanner/strict.py contrib/data/*/*/results.jsonl > contrib/data/STRICT.md
$ python -I contrib/scanner/strict.py --readme README.md contrib/data/*/*/results.jsonl
```

`strict.py` decides which features a strict parser rejects, in its tables `STRICT` and
`ALLOWED`: a policy is a change to those.

## Checking the scanner against the test suite

```console
$ python -I contrib/scanner/check_suite.py
```

checks that `tarscan.py` reports the features of every case of [suite/](../../suite), and that
the default policy of `strict.py` rejects the cases to reject and accepts the others.

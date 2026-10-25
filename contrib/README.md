# How the data was made

Everything that [suite/](../suite) does not need: the scanner and the scans of real tarballs,
the runs of implementations over the test suite, and the site. The numbers in the top-level
README and on the site are generated from these.

- [scanner/](scanner): the scanner, how to scan the tarballs of an ecosystem, the default policy
  (`strict.py`), and the check of both against the test suite.
- [data/](data): the scans, each with a `RUN.md` on how it was made, and what was found in them:
  [data/STRICT.md](data/STRICT.md) has the cost of every criterion, and
  [data/REPORT.md](data/REPORT.md) every feature.
- [matrix/](matrix): what implementations make of every case, and the programs that run them.
- `site.py`: writes the site in [docs/](../docs).

The `RUN.md` of each scan gives the commands as they were run, at the commit it names, before
these scripts moved here from `scanner/` and `corpus/`.

## What implementations make of it

```console
$ python -I contrib/matrix/matrix.py WORK
```

extracts every case of [suite/](../suite) with every implementation it finds, and writes
[matrix/matrix.json](matrix/matrix.json) and the table in [matrix/MATRIX.md](matrix/MATRIX.md) from
it. Libraries without an extractor, such as Go's `archive/tar`, list the members, which are then
applied in order. WORK contains the builds of the programs in `matrix/runners/`, whose dependencies
are pinned, and the extractions: each in a directory of its own, two levels below a directory that
catches what is written outside it. Run it in a throwaway directory, or a container, as some cases
escape in lenient extractors. It uses what is installed: GNU tar, the untar of live-bootstrap (with
git and a C compiler), bsdtar, BusyBox, 7-Zip, Python's `tarfile` with each of its filters, Go
(`archive/tar`, and containerd's `archive.Apply`), Rust, Haskell (cabal), .NET, Java (with the jars
of `matrix/runners/java/jars.txt`, which it downloads and checks), PHP (its `PharData`), R (its
`Rscript`), Ruby, Perl, Julia and Node.js (node-tar and tar-fs): each on PATH, or in an environment
variable of its name in capitals, such as `$JULIA` or `$RSCRIPT`. With `--only` and the names of
columns, only those implementations run, and the other columns of `matrix.json` are kept as they
are.

## The site

```console
$ python -I contrib/site.py docs contrib/data/*/*/results.jsonl
```

writes `docs/`, which https://stoppels.ch/tar/ serves as files: an index with the matrix,
and a page per case with its explanation, its block map and dump, how many tarballs of the scans
have its feature and how many of those the default policy rejects, and what every implementation
makes of it, from `matrix.json`. Plain HTML and CSS, without scripts, all of it generated. The `Seen
in:` of a case is written by hand: site.py fails if it says no tarball where the scans have its
feature, or names tarballs where they have none.
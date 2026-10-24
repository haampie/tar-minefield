# Scan of a sample of 5000 crates, 2026-10-25

A sample of the crates of crates.io, one version each: the latest of 2500 crates, and an older
version of 2500 other crates, as `run.py sample` takes them, in the order of the rank of crates by
seed 0. `crates_list.py` lists only the first crates by that rank, as many as the sample takes
from, which gives the sample of a list of all crates:

```console
$ git clone --depth 1 --filter=blob:none --no-checkout \
      https://github.com/rust-lang/crates.io-index index
$ git -C index ls-tree -r --name-only HEAD > paths.txt
$ python -I scanner/crates_list.py paths.txt 5000 0 | gzip -9 > ../lists/f16a3f865e54.jsonl.gz
$ gunzip -c ../lists/f16a3f865e54.jsonl.gz > list.jsonl
$ python -I scanner/run.py sample list.jsonl 5000 0 > sample.jsonl
$ TMPDIR=/tmp python -I scanner/run.py scan sample.jsonl results.jsonl --untar ~/untar --jobs 16
$ python -I scanner/report.py --title "Scan of a sample of 5000 crates" results.jsonl > REPORT.md
```

- Scanner: `tarscan.py` version `7078a34ab512`.
- Crates: the index of crates.io at `f16a3f865e548a8ea86e3b65737a74165bb4a682` (2026-10-24),
  360,901 crates, with their versions from the sparse index, index.crates.io. The latest version
  of a crate is its latest publication that is not yanked.
- untar: `2305390138cf436059b89b7b15146dc5213a3ba5`, `untar.py` version `51a9c3aa565c`.
- Platform: Ubuntu 26.04 (Linux 7.0) on x86_64, Python 3.14.4. untar extracted to tmpfs, which
  every crate fit in: it is case-sensitive, so no failures are caused by the filesystem.

Every crate was downloaded from static.crates.io and scanned, 0.77 GB and 188,075 members in all.
6 downloads failed with HTTP 500 and were tried again, after removing their rows, and then worked.
None of these crates is in the other scans.

# Scan of a sample of 5000 gems, 2026-10-25

A sample of the gems of RubyGems, one version each: the latest of 2500 gems, and an older version
of 2500 other gems, as `run.py sample` takes them, in the order of the rank of gems by seed 0.
`rubygems_list.py` lists only the first gems by that rank, as many as the sample takes from, which
gives the sample of a list of all gems:

```console
$ python -I scanner/rubygems_list.py 5000 0 | gzip -9 > ../lists/2026-10-24.jsonl.gz
$ gunzip -c ../lists/2026-10-24.jsonl.gz > list.jsonl
$ python -I scanner/run.py sample list.jsonl 5000 0 > sample.jsonl
$ TMPDIR=/tmp python -I scanner/run.py scan sample.jsonl results.jsonl --untar ~/untar --jobs 16
$ python -I scanner/report.py --title "Scan of a sample of 5000 gems" results.jsonl > REPORT.md
```

- Scanner: `tarscan.py` version `7078a34ab512`.
- Gems: the compact index of rubygems.org on 2026-10-24, its `versions` and the `info` of each
  gem: only versions for the platform `ruby`, the gems of sources. The latest version of a gem is
  its latest that the index has, which leaves out yanked versions.
- A gem is an uncompressed tar of `metadata.gz`, `data.tar.gz` and `checksums.yaml.gz`, written by
  RubyGems. The tarball scanned and extracted is `data.tar.gz`, the files a gem installs; the
  sha256 checked is that of the gem, and the features of the gem itself are in `member_of`.
- untar: `2305390138cf436059b89b7b15146dc5213a3ba5`, `untar.py` version `51a9c3aa565c`.
- Platform: Ubuntu 26.04 (Linux 7.0) on x86_64, Python 3.14.4. untar extracted to tmpfs, which
  every gem fit in: it is case-sensitive, so no failures are caused by the filesystem.

Every gem was downloaded from rubygems.org and scanned, 0.96 GB and 220,587 members of
`data.tar.gz` in all. None of these gems is in the other scans.

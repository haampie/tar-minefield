# Scan of a sample of 10000 PyPI sdists, 2026-10-24

A sample of PyPI's projects, one sdist each: the latest sdist of 5000 projects, and an older sdist
of 5000 other projects, as `run.py sample` takes them, in the order of the rank of projects by
seed 0. PyPI has about a million projects, so `pypi_list.py` lists only the first ones by that rank,
as many as the sample takes from (14000), which gives the sample of a list of all projects:

```console
$ python -I scanner/pypi_list.py 10000 0 | gzip -9 > ../lists/42699224.jsonl.gz
$ gunzip -c ../lists/42699224.jsonl.gz > list.jsonl
$ python -I scanner/run.py sample list.jsonl 10000 0 > sample.jsonl
$ TMPDIR=/tmp python -I scanner/run.py scan sample.jsonl results.jsonl --untar ~/untar --jobs 16
$ python -I scanner/report.py --title "Scan of a sample of 10000 PyPI sdists" results.jsonl > REPORT.md
```

- Scanner: `tarscan.py` version `7078a34ab512`.
- Projects: the simple index of PyPI (PEP 691 and PEP 700) at `_last-serial` 42699224, on
  2026-10-24. An sdist is a file of a project in a tar format, and the latest is its latest upload
  that is not yanked. One project's page, which the CDN served cut short every time, was read from
  the JSON API instead.
- untar: `2305390138cf436059b89b7b15146dc5213a3ba5`, `untar.py` version `51a9c3aa565c`.
- Platform: Ubuntu 26.04 (Linux 7.0) on x86_64, Python 3.14.4. untar extracted to tmpfs, which
  every sdist fit in: it is case-sensitive, so no failures are caused by the filesystem.

Every sdist was downloaded from files.pythonhosted.org and scanned, 7.9 GB and 722,380 members in
all. `--reuse` copies nothing here, as the other scans are of earlier versions of the scanner; 35
of these sdists are also in them.

"""List the crates of crates.io, as JSON lines, in the order of run.py's sample.

    git clone --depth 1 --filter=blob:none --no-checkout \
        https://github.com/rust-lang/crates.io-index index
    git -C index ls-tree -r --name-only HEAD > paths.txt
    python -I contrib/scanner/crates_list.py paths.txt N SEED > crates.jsonl

The paths of the index are the names of all crates, without their contents. Like pypi_list.py,
this lists only as many crates as `run.py sample LIST N SEED` takes from, in the order of their
rank by SEED, with their versions from the sparse index, index.crates.io, and downloads from
static.crates.io. A package is a crate, by its name in lower case, and its latest version is its
latest publication that is not yanked. A yanked version is listed as deprecated.
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from run import fetch, list_ranked  # noqa: E402

INDEX = "https://index.crates.io/"
STATIC = "https://static.crates.io/crates/"


def crates(path):
    """The versions of the crate at path in the index, as run.py takes them."""
    lines = [json.loads(line) for line in fetch(INDEX + path).decode().splitlines() if line]
    # in the order of publication, which the index has where a version has no pubtime
    versions = sorted(enumerate(lines), key=lambda iv: (iv[1].get("pubtime") or "", iv[0]))
    versions = [v for _, v in versions]
    latest = next((v for v in reversed(versions) if not v["yanked"]), None)
    return [{
        "package": v["name"].lower(),
        "version": v["vers"],
        "sha256": v["cksum"],
        "url": f"{STATIC}{v['name']}/{v['name']}-{v['vers']}.crate",
        "urls": [f"{STATIC}{v['name']}/{v['name']}-{v['vers']}.crate"],
        "deprecated": v["yanked"],
        "latest": v is latest,
        "upload_time": v.get("pubtime"),
    } for v in versions]


def main():
    paths, n, seed = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    by_name = {}
    for line in open(paths):
        path = line.strip()
        if path and "/" in path and not path.startswith("."):
            by_name[path.rsplit("/", 1)[1]] = path
    list_ranked(list(by_name), lambda name: crates(by_name[name]), n, seed)


if __name__ == "__main__":
    main()

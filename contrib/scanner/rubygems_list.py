"""List the gems of RubyGems, as JSON lines, in the order of run.py's sample.

    python -I contrib/scanner/rubygems_list.py N SEED > rubygems.jsonl

The names of all gems come from the compact index, rubygems.org/versions, whose `created_at` is
written to stderr. Like pypi_list.py, this lists only as many gems as `run.py sample LIST N SEED`
takes from, in the order of their rank by SEED, with their versions from rubygems.org/info: only
those of the platform `ruby`, the gems of sources rather than of builds for one platform. A gem
is an uncompressed tar, whose member `data.tar.gz` contains the files a gem installs: that is the
tarball scanned, and the sha256 is that of the gem. A package is a gem, and its latest version
is its latest that the index has, which leaves out yanked versions.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from run import fetch, list_ranked  # noqa: E402

INDEX = "https://rubygems.org/"


def gems(name):
    """The versions of a gem of the platform `ruby`, as run.py takes them."""
    versions = []
    for line in fetch(f"{INDEX}info/{name}").decode().split("---\n", 1)[-1].splitlines():
        version, _, rest = line.partition(" ")
        # a version for another platform ends in it: 1.0-x86_64-linux
        if not version or "-" in version:
            continue
        info = dict(kv.split(":", 1) for kv in rest.split("|", 1)[-1].split(",") if ":" in kv)
        if "checksum" in info:
            versions.append((info.get("created_at") or "", version, info["checksum"]))
    versions.sort()
    return [{
        "package": name,
        "version": version,
        "sha256": sha256,
        "url": f"{INDEX}gems/{name}-{version}.gem",
        "urls": [f"{INDEX}gems/{name}-{version}.gem"],
        "member": "data.tar.gz",
        "deprecated": False,
        "latest": i == len(versions) - 1,
        "upload_time": created or None,
    } for i, (created, version, sha256) in enumerate(versions)]


def main():
    n, seed = int(sys.argv[1]), sys.argv[2]
    head, _, body = fetch(f"{INDEX}versions").decode().partition("---\n")
    print(head.strip(), file=sys.stderr)
    names = {line.split(" ", 1)[0] for line in body.splitlines() if line}
    list_ranked(sorted(names), gems, n, seed)


if __name__ == "__main__":
    main()

"""List the sdists of PyPI projects, as JSON lines, in the order of run.py's sample.

    python -I contrib/scanner/pypi_list.py N SEED > pypi.jsonl

PyPI has about a million projects, so this lists only as many as `run.py sample LIST N SEED`
takes from: projects in the order of their rank by SEED, until N/2 of them have a latest sdist
and N/2 of the others an older one. As the rank of a project does not depend on the others, the
sample of this list is the sample of a list of all projects.

The projects and their files come from the JSON of the simple index (PEP 691 and PEP 700), whose
`_last-serial` is written to stderr, and from the JSON API for the few projects whose page the CDN
serves cut short. Sdists are files of a project in a tar format; quarantined
projects are left out. A package is a project, by its normalized name, and its latest version is
its latest sdist upload that is not yanked. A yanked sdist is listed as deprecated.
"""

import concurrent.futures
import http.client
import json
import os
import re
import sys
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from run import USER_AGENT, rank  # noqa: E402

INDEX = "https://pypi.org/simple/"
TAR = re.compile(r"\.(tar|tar\.gz|tgz|tar\.bz2|tbz2|tar\.xz|txz)$", re.IGNORECASE)


def get(url, accept="application/vnd.pypi.simple.v1+json"):
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": accept})
    for attempt in range(5):
        try:
            with urllib.request.urlopen(request, timeout=60) as r:
                return json.load(r)
        except (OSError, ValueError, http.client.HTTPException):
            # also a response cut short, which is not valid JSON
            if attempt == 4:
                raise


def files_of(name):
    """The project's page of the simple index, or, where the CDN serves that cut short every time,
    as it does some, its files from the JSON API in the same form."""
    try:
        return get(f"{INDEX}{name}/")
    except ValueError:
        project = get(f"https://pypi.org/pypi/{name}/json", accept="application/json")
        return {"files": [
            {"filename": f["filename"], "hashes": f["digests"], "url": f["url"],
             "upload-time": f["upload_time_iso_8601"], "size": f["size"], "yanked": f["yanked"]}
            for files in project["releases"].values() for f in files]}


def normalize(name):
    return re.sub(r"[-_.]+", "-", name).lower()


def version(name, filename):
    """The version of an sdist by its file name: what follows the project's name and a dash."""
    stem = TAR.sub("", filename)
    for i, c in enumerate(stem):
        if c == "-" and normalize(stem[:i]) == normalize(name):
            return stem[i + 1:]
    return stem.rsplit("-", 1)[-1]


def sdists(name):
    """The sdists of a project, as run.py takes them, or none if it is quarantined."""
    project = files_of(name)
    if (project.get("project-status") or {}).get("status") == "quarantined":
        return []
    files = sorted((f for f in project["files"] if TAR.search(f["filename"])),
                   key=lambda f: f["upload-time"] or "")
    latest = next((f for f in reversed(files) if not f.get("yanked")), None)
    return [{
        "package": name,
        "version": version(name, f["filename"]),
        "sha256": f["hashes"]["sha256"],
        "url": f["url"],
        "urls": [f["url"]],
        "deprecated": bool(f.get("yanked")),
        "latest": f is latest,
        "upload_time": f["upload-time"],
        "size": f.get("size"),
    } for f in files if "sha256" in f["hashes"]]


def main():
    n, seed = int(sys.argv[1]), sys.argv[2]
    index = get(INDEX)
    print(f"_last-serial {index['meta']['_last-serial']}", file=sys.stderr)
    names = sorted((p["name"] for p in index["projects"]), key=lambda p: rank(seed, p))
    latest, older = 0, 0
    with concurrent.futures.ThreadPoolExecutor(8) as pool:
        # in batches, in order, so that the list stops where the sample does
        for start in range(0, len(names), 400):
            for files in pool.map(sdists, names[start:start + 400]):
                if latest < n // 2:
                    latest += any(f["latest"] for f in files)
                elif older < n - n // 2:
                    older += any(not f["latest"] for f in files)
                else:
                    continue
                for f in files:
                    print(json.dumps(f))
            print(f"{start + 400} projects: {latest} latest, {older} older", file=sys.stderr)
            if latest >= n // 2 and older >= n - n // 2:
                break


if __name__ == "__main__":
    main()

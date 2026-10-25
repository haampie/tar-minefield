"""List the tarballs of nixpkgs, as JSON lines.

In a checkout of nixpkgs:

    nix-instantiate --eval --json --strict maintainers/scripts/find-tarballs.nix \
        --arg expr 'import ./maintainers/scripts/all-tarballs.nix' > files.json
    nix-instantiate --eval --json --strict -E \
        'removeAttrs (import ./pkgs/build-support/fetchurl/mirrors.nix) [ "hashedMirrors" ]' \
        > mirrors.json
    python -I contrib/scanner/nix_list.py mirrors.json files.json... > nix.jsonl

find-tarballs.nix lists the files that the Hydra jobs of nixpkgs fetch with a flat hash, as
fetchurl does: not those of fetchzip or fetchFromGitHub, which hash the unpacked tree. Evaluating
all jobs at once takes over 10 GB of memory, so they can be evaluated in chunks instead, each a
list of jobs as `expr`, and the outputs passed together. Evaluation needs no Nix daemon, and with
`--readonly-mode` writes nothing to the store.

Only tarballs with a sha256 are listed, and not those changed after the download (postFetch).
Their URLs are tarballs.nixos.org first, then those of the fetchurl call, with mirror:// URLs
resolved to the first two mirrors of mirrors.json. A package is the name of the tarball up to its
version, and its latest version is the highest version of it in nixpkgs.
"""

import base64
import json
import re
import sys

TARBALLS = "https://tarballs.nixos.org/sha256"
TAR = re.compile(r"\.(tar|tar\.gz|tgz|tar\.bz2|tbz2|tbz|tar\.xz|txz|tar\.lzma|tar\.lz|tar\.zst)$")
# Nix's base32, which leaves out e, o, u and t
BASE32 = "0123456789abcdfghijklmnpqrsvwxyz"


def from_base32(s):
    """Decode Nix's base32, in which the last character encodes the lowest bits."""
    out = bytearray(len(s) * 5 // 8)
    for n, c in enumerate(reversed(s)):
        digit = BASE32.index(c)
        i, j = divmod(n * 5, 8)
        out[i] |= (digit << j) & 0xFF
        if i + 1 < len(out):
            out[i + 1] |= digit >> (8 - j)
    return bytes(out)


def sha256_hex(file):
    """The sha256 of a file of find-tarballs.nix in hex, or None if it has another hash."""
    h, algo = file["hash"], file["type"]
    if h.startswith("sha256-"):
        digest = from_base64(h[7:])
    elif algo != "sha256":
        return None
    elif len(h) == 64:
        return h.lower()
    elif len(h) == 52:
        digest = from_base32(h)
    else:
        digest = from_base64(h)
    return digest.hex() if digest is not None and len(digest) == 32 else None


def from_base64(s):
    """Decode base64 with any padding, which Nix accepts."""
    s = s.rstrip("=")
    try:
        return base64.b64decode(s + "=" * (-len(s) % 4), validate=True)
    except ValueError:
        return None


def resolve(url, mirrors):
    """The URLs to download url from: a mirror:// URL is one per mirror."""
    m = re.match(r"^mirror://([^/]+)/(.*)$", url)
    if not m:
        return [url]
    return [base + m.group(2) for base in mirrors.get(m.group(1), [])[:2]]


def package_version(name):
    stem = TAR.sub("", name)
    m = re.match(r"^(.+?)-(v?\d.*)$", stem) or re.match(r"^([A-Za-z]+)(\d.*)$", stem)
    return (m.group(1), m.group(2)) if m else (stem, "")


def version_key(version):
    """Order versions by their numbers first: 1.10 after 1.9."""
    return [(0, int(p)) if p.isdigit() else (1, p) for p in re.split(r"(\d+)", version) if p]


def main():
    mirrors = json.load(open(sys.argv[1]))
    tarballs = {}
    for path in sys.argv[2:]:
        for file in json.load(open(path)):
            name = file["name"]
            basename = file["urls"][0].split("?")[0].rsplit("/", 1)[-1] if file["urls"] else ""
            if file["isPatch"] or not (TAR.search(name) or TAR.search(basename)):
                continue
            sha256 = sha256_hex(file)
            if sha256 is None or sha256 in tarballs:
                continue
            if not TAR.search(name):
                name = basename
            urls = [u for url in file["urls"] for u in resolve(url, mirrors)]
            urls = [u for u in urls if u.startswith(("https://", "http://", "ftp://"))]
            package, version = package_version(name)
            tarballs[sha256] = {
                "package": package,
                "version": version,
                "sha256": sha256,
                "url": urls[0] if urls else file["urls"][0],
                "urls": [f"{TARBALLS}/{sha256}"] + urls,
                "name": name,
            }
    latest = {}
    for t in tarballs.values():
        best = latest.get(t["package"])
        if best is None or version_key(t["version"]) > version_key(best["version"]):
            latest[t["package"]] = t
    for sha256 in sorted(tarballs):
        t = tarballs[sha256]
        t["latest"] = latest[t["package"]] is t
        print(json.dumps(t))


if __name__ == "__main__":
    main()

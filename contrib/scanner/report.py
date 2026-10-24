"""Summarize the output of run.py as Markdown.

    python -I contrib/scanner/report.py [--title TITLE] RESULTS... > REPORT.md

With several results files, features and producers are counted over the distinct tarballs (by
sha256) of all of them, and rates are given per file: each file is a sample of its own
population, so its rates do not pool with others. A file is named by its directory under data/.
"""

import collections
import contextlib
import io
import json
import os
import re
import sys
import time
import urllib.parse


def origin(url):
    host = url.split("/")[2]
    if host in ("github.com", "codeload.github.com"):
        return "github-release" if "/releases/download/" in url else "github-archive"
    if host in ("gitlab.com",) or "gitlab" in host:
        return "gitlab"
    if host in ("files.pythonhosted.org", "pypi.io", "pypi.org"):
        return "pypi"
    if "cran" in host or "r-project.org" in host or "bioconductor" in host:
        return "cran/bioconductor"
    if "cpan" in host:
        return "cpan"
    if host in ("static.crates.io", "crates.io"):
        return "crates.io"
    if host in ("rubygems.org", "index.rubygems.org"):
        return "rubygems"
    if "gnu.org" in host or url.split("/")[3:4] == ["gnu"]:
        return "gnu"
    return "other"


def producer(r):
    fp = r.get("fingerprint", {})
    if fp.get("producer_hint", {}).get("git-archive"):
        return "git archive"
    pax = fp.get("pax_header_name", {})
    if any("PaxHeaders" in k for k in pax):
        return "GNU tar (pax)"
    if any("PaxHeader/" in k for k in pax):
        return "libarchive (pax)"
    if any("@PaxHeader" in k for k in pax):
        return "Python tarfile (pax)"
    magic = fp.get("magic", {})
    top = max(magic, key=magic.get) if magic else "none"
    return {"gnu": "GNU format", "posix": "ustar", "v7": "v7"}.get(top, top)


def year(r):
    m = r.get("mtime")
    if not m:
        return None
    try:
        return time.gmtime(m[1]).tm_year
    except (OverflowError, OSError, ValueError):
        return None


def untar_reason(error):
    error = re.sub(r"'[^']*'|\"[^\"]*\"", "'…'", error)
    error = re.sub(
        r"(symlink|path|contains|through|Archive contains) \S+(?= (twice|without|which|named|more))",
        r"\1 …",
        error,
    )
    error = re.sub(r"unsafe path .*", "unsafe path …", error)
    error = re.sub(r"\d+", "N", error)
    return error


def filesystem_only(r):
    """Whether untar failed only because the scanning machine's filesystem cannot hold the tree:
    names that collide there, and no duplicates in the archive itself."""
    features = r.get("features", {})
    collides = any(
        f in features for f in ("platform.case-collision", "platform.normalization-collision")
    )
    duplicates = any(f.startswith("tree.duplicate.") for f in features)
    error = r.get("untar_error") or ""
    return (
        collides
        and not duplicates
        and (error.startswith("FileExistsError") or "which is not a directory" in error)
    )


def counter(c, n=4):
    return ", ".join(f"{k} {v}" for k, v in c.most_common(n))


# Ecosystems as the reports name them, by the directory of their scans, in the order they name them
ECOSYSTEMS = {"spack": "Spack", "nix": "nixpkgs", "guix": "Guix", "live-bootstrap": "live-bootstrap",
              "pypi": "PyPI", "crates": "crates.io", "rubygems": "RubyGems"}


def ecosystems(names):
    """The ecosystems of datasets, by their names, as text, such as "Spack, nixpkgs and Guix"."""
    dirs = sorted({n.split("/")[0] for n in names},
                  key=lambda d: (list(ECOSYSTEMS).index(d) if d in ECOSYSTEMS else len(ECOSYSTEMS), d))
    words = [ECOSYSTEMS.get(d, d) for d in dirs]
    return ", ".join(words[:-1]) + " and " + words[-1] if len(words) > 1 else "".join(words)


def dataset_name(path):
    parts = os.path.abspath(path).split(os.sep)
    if "data" in parts[:-1]:
        return "/".join(parts[len(parts) - parts[::-1].index("data") : -1])
    return path


def upgrade_magic(r):
    """A result of tarscan.py from before it told NULs as the version of the POSIX magic apart from
    other versions, which it reported as one feature, with the features it reports now: the
    fingerprint has the headers of each version."""
    old = "magic.posix-with-odd-version"
    if old not in r.get("features", {}) or r.get("fingerprint", {}).get("magic") is None:
        return r
    magic = r["fingerprint"]["magic"]
    nuls = magic.get("posix-version-0000", 0)
    odd = sum(n for m, n in magic.items() if m.startswith("posix-version-")) - nuls
    features = {f: n for f, n in r["features"].items() if f != old}
    examples = dict(r.get("examples") or {})
    if nuls:
        features["magic.posix-version-nuls"] = nuls
        if not odd and old in examples:
            examples["magic.posix-version-nuls"] = examples.pop(old)
    if odd:
        features[old] = odd
    return dict(r, features=features, examples=examples)


def upgrade_chksum(r):
    """A result of tarscan.py from before it reported checksums padded with leading spaces, with
    that feature: the fingerprint has the headers of each shape of the checksum field."""
    feature = "number.chksum.leading-space"
    if feature in r.get("features", {}) or r.get("fingerprint", {}).get("checksum") is None:
        return r
    n = sum(k for shape, k in r["fingerprint"]["checksum"].items()
            if shape.startswith("s") and "d" in shape)
    return dict(r, features=dict(r["features"], **{feature: n})) if n else r


def upgrade(r):
    """A result of an earlier version of tarscan.py with the features it reports now, as far as
    its fingerprint tells them."""
    return upgrade_chksum(upgrade_magic(r))


def load(paths):
    """The distinct tarballs of all results files, each with the datasets it is in; and the rows
    of each file."""
    union = {}
    datasets = {}
    for path in paths:
        name = dataset_name(path)
        datasets[name] = [upgrade(json.loads(line)) for line in open(path)]
        for r in datasets[name]:
            if r["sha256"] in union:
                u = union[r["sha256"]]
                u["datasets"].append(name)
                u["latest"] = u.get("latest") or r.get("latest")
                if "features" in r and "features" not in u:
                    union[r["sha256"]] = dict(r, datasets=u["datasets"], latest=u["latest"])
            else:
                union[r["sha256"]] = dict(r, datasets=[name])
    return list(union.values()), datasets


def dataset_table(datasets):
    print("| ecosystem | tarballs | scanned | latest | untar rejects | latest | filesystem only |")
    print("|---|---|---|---|---|---|---|")
    for name, rows in datasets.items():
        scanned = [r for r in rows if "features" in r]
        latest = [r for r in scanned if r.get("latest")]
        rejected = [r for r in scanned if r.get("untar_error") and not filesystem_only(r)]
        rl = [r for r in rejected if r.get("latest")]
        local = [r for r in scanned if r.get("untar_error") and filesystem_only(r)]
        tested = [r for r in scanned if "untar" in r or "untar_error" in r]
        if not tested:
            print(f"| {name} | {len(rows)} | {len(scanned)} | {len(latest)} | | | |")
            continue
        print(
            f"| {name} | {len(rows)} | {len(scanned)} | {len(latest)} | {len(rejected)} "
            f"({percent(len(rejected), len(scanned))}) | {len(rl)} "
            f"({percent(len(rl), len(latest))}) | {len(local)} |"
        )


def percent(n, total):
    return f"{100 * n / total:.2f}%" if total else "–"


# A cell of a number, or of a count and its share, such as `10,168`, `76.5` or `28 (0.28%)`
NUMBER = re.compile(r"[\d,]+(\.\d+)?( \(\d+(\.\d+)?%\))?|–")


def tidy_tables(text):
    """Markdown with the columns of its tables that hold only numbers right-aligned, and those
    numbers with thousands separators."""
    lines, out, i = text.split("\n"), [], 0
    while i < len(lines):
        if not (lines[i].startswith("|") and i + 1 < len(lines)
                and re.fullmatch(r"\|(---\|)+", lines[i + 1])):
            out.append(lines[i])
            i += 1
            continue
        j = i + 2
        while j < len(lines) and lines[j].startswith("| "):
            j += 1
        rows = [line[2:-2].split(" | ") for line in lines[i + 2:j]]
        width = lines[i + 1].count("---")
        numeric = [bool(rows) and all(c < len(r) and NUMBER.fullmatch(r[c]) for r in rows)
                   for c in range(width)]
        out += [lines[i], "|" + "".join("---:|" if n else "---|" for n in numeric)]
        for r in rows:
            cells = [re.sub(r"(?<![\d.,])\d{4,}(?!\d)", lambda m: f"{int(m.group()):,}", cell)
                     if c < width and numeric[c] else cell for c, cell in enumerate(r)]
            out.append("| " + " | ".join(cells) + " |")
        i = j
    return "\n".join(out)


def main():
    args = sys.argv[1:]
    title = "Scan of tarballs"
    if args[:1] == ["--title"]:
        title, args = args[1], args[2:]
    rows, datasets = load(args)
    scanned = [r for r in rows if "features" in r]
    failed = [r for r in rows if "download_error" in r]
    crashed = [r for r in rows if "scan_crash" in r]
    latest = sum(1 for r in scanned if r.get("latest"))

    print(f"# {title}\n")
    if len(datasets) > 1:
        print(
            "Rates are per ecosystem. Counts below are of the distinct tarballs of all ecosystems.\n"
        )
        dataset_table(datasets)
        print()
    print(
        f"- tarballs: {len(rows)}, scanned: {len(scanned)} ({latest} latest versions, "
        f"{len(scanned) - latest} older)"
    )
    print(f"- not downloaded: {len(failed)}, scanner crashed: {len(crashed)}")
    first = sum(r.get("source") in ("mirror", (r.get("urls") or [None])[0]) for r in scanned)
    print(f"- downloaded from the first of their URLs (a mirror): {first}")
    hosts = collections.Counter(urllib.parse.urlsplit(r.get("source") or "").netloc for r in scanned)
    print(
        f"- copied from other scans with `--reuse`: {sum(1 for r in scanned if r.get('reused'))}, "
        f"read from `--cache`: {sum(1 for r in scanned if r.get('cached'))}; "
        f"sources by host: {counter(hosts, 6)}"
    )
    print(f"- size: {sum(r.get('bytes', 0) for r in scanned) / 1e9:.1f} GB compressed")
    print(f"- origins: {counter(collections.Counter(origin(r['url']) for r in scanned), 10)}")
    print(f"- producers: {counter(collections.Counter(producer(r) for r in scanned), 10)}")
    print(
        f"- compression: {counter(collections.Counter(r['compression']['format'] for r in scanned))}"
    )
    for r in scanned:
        if r.get("compression_error"):
            print(
                f"- compression error in {r['package']}@{r['version']}: {r['compression_error']}"
            )
    errors = [r for r in scanned if r.get("error")]
    print(f"- scanner stopped early: {len(errors)}")
    for r in errors:
        print(f"  - {r['package']}@{r['version']}: {r['error']}")

    if any("untar_error" in r for r in scanned):
        skipped = [r for r in scanned if r.get("untar_skipped")]
        for r in skipped:
            print(f"- untar skipped {r['package']}@{r['version']}: {r['untar_skipped'][:200]}")
        local = [r for r in scanned if r.get("untar_error") and filesystem_only(r)]
        if local:
            print(
                f"\nFailed only because of the case-insensitive filesystem of the scanning "
                f"machine, not counted as rejections: {len(local)}, "
                f"{sum(r.get('latest', False) for r in local)} latest "
                f"({'; '.join(r['package'] + '@' + r['version'] for r in local[:6])})."
            )
        rejected = [r for r in scanned if r.get("untar_error") and not filesystem_only(r)]
        rl = sum(1 for r in rejected if r.get("latest"))
        print(
            f"\n## untar\n\nRejects {len(rejected)} of {len(scanned)} "
            f"({100 * len(rejected) / len(scanned):.1f}%); "
            f"{rl} of {latest} latest versions ({100 * rl / max(latest, 1):.1f}%).\n"
        )
        print("| reason | tarballs | latest | origins | producers | examples |")
        print("|---|---|---|---|---|---|")
        by_reason = collections.defaultdict(list)
        for r in rejected:
            by_reason[untar_reason(r["untar_error"])].append(r)
        for reason, rs in sorted(by_reason.items(), key=lambda kv: -len(kv[1])):
            examples = "; ".join(f"{r['package']}@{r['version']}" for r in rs[:3])
            print(
                f"| {reason.replace('|', '/')} | {len(rs)} | {sum(r.get('latest', False) for r in rs)} | "
                f"{counter(collections.Counter(origin(r['url']) for r in rs), 3)} | "
                f"{counter(collections.Counter(producer(r) for r in rs), 3)} | {examples} |"
            )

    print("\n## Features\n")
    print(
        "Number of tarballs with each feature, of which latest versions; their origins, "
        "producers and median mtime years, and what untar did with them.\n"
    )
    print(
        "| feature | tarballs | latest | origins | producers | years | untar rejects | examples |"
    )
    print("|---|---|---|---|---|---|---|---|")
    by_feature = collections.defaultdict(list)
    for r in scanned:
        for f in r["features"]:
            by_feature[f].append(r)
    for f, rs in sorted(by_feature.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        years = sorted(y for y in map(year, rs) if y)
        span = f"{years[0]}–{years[-1]}" if years else ""
        # a feature that upgrade translated from the fingerprint has no example member
        examples = "; ".join(
            f"{r['package']}@{r['version']}"
            + (f" `{r['examples'][f][0][:60]}`" if r["examples"].get(f) else "")
            for r in rs[:2]
        ).replace("|", "/")
        print(
            f"| `{f}` | {len(rs)} | {sum(r.get('latest', False) for r in rs)} | "
            f"{counter(collections.Counter(origin(r['url']) for r in rs), 3)} | "
            f"{counter(collections.Counter(producer(r) for r in rs), 3)} | {span} | "
            f"{sum(1 for r in rs if r.get('untar_error'))} | {examples} |"
        )

    print("\n## Fingerprints\n")
    for key in (
        "magic",
        "size",
        "mode",
        "checksum",
        "pax_header_name",
        "extended_sequence",
        "gnu_long_name",
        "end",
        "zero_blocks_after_end",
        "pax_keys",
        "pax_global_keys",
    ):
        c = collections.Counter()
        for r in scanned:
            for k in r.get("fingerprint", {}).get(key, {}):
                if key == "pax_header_name":
                    k = re.sub(r"[0-9a-fN]{16,}", "H", k)
                c[k] += 1
        print(f"- {key} (tarballs using each): {counter(c, 12)}")
    c = collections.Counter()
    for r in scanned:
        info = r["compression"]
        if info.get("streams", 0) > 1:
            c["several streams"] += 1
        if info.get("trailing_bytes"):
            c["trailing nonzero" if info.get("trailing_nonzero") else "trailing zeros"] += 1
        if info.get("truncated"):
            c["truncated"] += 1
    print(f"- compression layer: {counter(c)}")


if __name__ == "__main__":
    with contextlib.redirect_stdout(io.StringIO()) as out:
        main()
    print(tidy_tables(out.getvalue()), end="")

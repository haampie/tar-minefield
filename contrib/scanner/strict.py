"""How many real tarballs a strict parser would reject, as Markdown.

    python -I contrib/scanner/strict.py RESULTS... > STRICT.md
    python -I contrib/scanner/strict.py --readme README.md RESULTS...

A strict parser rejects every archive with a feature that METHOD.md lists as an ambiguity: the
criteria below, each a pattern of feature names of tarscan.py. Features of the cases that
METHOD.md lists to accept, or that are confined to fields outside the tree it describes, are
allowed. Names that some filesystems cannot hold (`platform.*`) are neither: they are reported
apart. A feature that none of these patterns match is reported as unclassified, so that nothing is
left out unseen.

The default policy, `DEFAULT`, is what METHOD.md decides from these scans: it normalizes some of
the criteria and accepts others, and rejects the rest. What each rejects is given of both.

Each results file is the scan of an ecosystem, and rates are given per ecosystem: each is a
sample of its own population. Tarballs in a compression that tarscan.py does not read are not assessed.

With --readme, the sentence between the markers `<!-- begin strict.py -->` and
`<!-- end strict.py -->` in that file, which may be inside a paragraph, is generated again, and
nothing else is printed: so that no number in it is written by hand.
"""

import collections
import contextlib
import fnmatch
import functools
import io
import os
import re
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from report import ecosystems, load, origin, tidy_tables  # noqa: E402

SITE = "https://stoppels.ch/tar/"

CATEGORIES = ("framing", "name", "kind", "order and state")

# (pattern, category, what it means), in order: the first pattern that matches a feature applies.
STRICT = [
    ("scan.error", "framing", "the scanner could not read past a header"),
    ("checksum.*", "framing", "a checksum that matches only one way of summing"),
    # Number fields that shape the tree are one criterion per problem: see criterion()
    ("number.[*].*", "framing",
     "a size, mode or checksum written in a way that implementations differ on"),
    ("number.size.*", "framing", "a size written in a way that implementations differ on"),
    ("number.chksum.*", "framing",
     "a checksum field written in a way that implementations differ on"),
    ("magic.posix-version-nuls", "framing", "POSIX magic with NULs as its version"),
    ("magic.posix-with-odd-version", "framing", "POSIX magic with a version other than `00` or NULs"),
    ("magic.*", "framing", "a header that implementations may not recognize as one"),
    ("type.unknown-*", "framing", "an unknown typeflag: data or no data"),
    ("type.gnu-sparse", "framing", "GNU's old sparse files"),
    ("type.contiguous", "framing", "contiguous files (7)"),
    ("pax.invalid-size", "framing", "a pax size that is not a number"),
    ("pax.size-leading-zero", "framing",
     "a pax size with leading zeros, which a reader may take as octal"),
    ("pax.size-too-large", "framing",
     "a pax size of 2^63 or more, which readers wrap, cut or reject"),
    ("pax.size-on-*", "framing", "a pax size on a member without data"),
    ("size.on-*", "framing", "a size on a member without data, which some implementations skip"),
    ("pax.size-*", "framing", "a pax size that disagrees with the header"),
    ("extended.pax-size-before-gnu-long", "framing", "a pax size that a GNU long name may take"),
    ("extended.without-member", "framing", "an extended header without a member"),
    ("pax-global.between-extended-and-member", "framing",
     "a global header between an extended header and its member"),
    ("pax-global.after-members", "framing", "a global header after the first member"),
    ("pax-global.size", "framing", "a size in a global header"),
    ("pax.newline-in-value.*", "framing",
     "a newline in a pax value, where implementations split lines"),
    ("pax.invalid-length", "framing", "a pax record whose length is not a number, or is wrong"),
    ("pax.length-leading-zero", "framing", "a pax record whose length has leading zeros"),
    ("pax.trailing-nuls", "framing", "NULs after the last pax record"),
    ("pax.no-newline", "framing", "a pax record that does not end in a newline"),
    ("pax.no-equals", "framing", "a pax record without `=`"),
    ("pax.empty-key", "framing", "a pax record with an empty key"),
    ("pax.empty-value.size", "framing", "an empty pax size, which in POSIX removes it"),
    ("end.missing", "framing", "no end-of-archive marker"),
    ("end.lone-zero-block", "framing", "an end-of-archive marker of one zero block, not two"),
    ("end.data-after", "framing", "data other than zeros after the end-of-archive marker"),
    ("end.archive-after", "framing", "another archive after the end-of-archive marker"),
    ("end.zero-block-before-member", "framing", "a zero block, then more members"),
    ("end.*", "framing", "the end of the archive"),
    ("archive.empty", "framing", "no members at all"),
    ("name.leading-dot-slash", "name", "a name like `./a`, which some implementations make `a`"),
    ("name.dot", "name", "a member named `.` or `./`"),
    ("name.dot-component", "name", "a name like `a/./b`"),
    ("name.double-slash", "name", "a name like `a//b`"),
    ("name.trailing-slash-on-file", "kind", "a regular file named like a directory, `a/`"),
    ("name.trailing-slash-on-*", "kind", "a link whose name ends in a slash"),
    ("name.absolute", "name", "an absolute name"),
    ("name.dotdot", "name", "a name with `..`"),
    ("name.empty", "name", "an empty name"),
    ("name.backslash", "name", "a backslash, `\\`, which is a separator on Windows"),
    ("name.drive-letter", "name", "a drive letter"),
    ("name.control-character", "name", "a control character in a name"),
    ("name.not-utf8", "name", "a name that is not UTF-8"),
    ("name.bytes-after-nul", "name", "bytes after the NUL that ends a name"),
    ("name.*", "name", "a name that implementations may normalize differently"),
    ("extended.gnu-long-and-pax", "name",
     "a GNU long name or link and a pax header for one member, which may apply to the other"),
    ("extended.*", "name", "several sources for one name or link target"),
    ("pax.hdrcharset", "name", "names that are not UTF-8 by declaration"),
    ("pax.path-not-utf8", "name", "a pax path that is not UTF-8"),
    ("pax.gnu-sparse", "name", "pax keys of GNU sparse files, which change the name"),
    ("pax.GNU.sparse.*", "name", "pax keys of GNU sparse files, which change the name"),
    ("pax.key-in-two-headers.*", "name", "a pax key in two extended headers of one member"),
    ("pax.repeated-key", "name", "a pax key twice in one extended header"),
    ("pax.nul-in-value.path", "name", "NUL in a pax path"),
    ("pax.nul-in-value.linkpath", "name", "NUL in a pax link path"),
    ("pax.key-whitespace", "name", "whitespace around a pax key, which GNU tar strips"),
    ("pax.empty-value.*", "name", "an empty pax value, which in POSIX removes the key"),
    ("pax.value-not-utf8.*", "name", "a pax value that is not UTF-8, which POSIX does not allow"),
    ("pax-global.path", "name", "a path in a global header"),
    ("pax-global.linkpath", "name", "a link path in a global header"),
    ("pax-global.empty-value.*", "name", "an empty value in a global header, which removes one"),
    ("pax-global.repeated-key", "name", "a pax key twice in one global header"),
    ("pax-global.nul-in-value.*", "name", "NUL in a value of a global header"),
    ("gnu.*", "name", "the prefix field of a GNU header, which GNU tar uses for times"),
    ("format.star", "name", "star's prefix field"),
    ("type.solaris-extended", "name", "Solaris X headers"),
    ("symlink.absolute", "name", "a symlink to an absolute path"),
    ("symlink.escapes", "name", "a symlink that points out of the archive"),
    ("symlink.*", "name", "a symlink target that implementations may handle differently"),
    ("pax.SCHILY.filetype", "kind", "a pax key that changes the kind"),
    ("linkname.on-*", "kind", "a link target on a member that is not a link"),
    ("number.mode.*", "kind", "a mode written in a way that implementations differ on"),
    ("tree.duplicate.file-file", "order and state", "the same file twice"),
    ("tree.duplicate.*", "order and state", "one path as two members"),
    ("tree.under-*", "order and state", "a member under a file or a symlink"),
    ("tree.through-symlink", "order and state", "a member written through a symlink"),
    ("tree.*", "order and state", "members that interact"),
    ("hardlink.to-itself", "order and state", "a hardlink to itself"),
    ("hardlink.to-symlink", "order and state", "a hardlink to a symlink"),
    ("hardlink.*", "order and state", "a hardlink to a later member, no member, or a misspelling"),
    ("pax-global.*", "framing",
     "records of a global header that implementations may split differently"),
]

ALLOWED = [
    ("name.fills-field", "a name of exactly 100 bytes, without NUL (to accept)"),
    ("linkname.no-nul", "a link name of exactly 100 bytes, without NUL"),
    ("name.non-ascii", "UTF-8 names"),
    ("name.not-nfc", "names not in NFC: one tree, which macOS may not hold"),
    ("name.dir-without-trailing-slash", "a directory without a trailing slash: the typeflag says"),
    ("ustar.prefix", "the ustar prefix field (to accept)"),
    ("number.size.base256", "base-256 sizes of files over 8 GiB (to accept)"),
    ("number.*.leading-space",
     "octal padded with spaces, not zeros, which implementations read alike"),
    ("number.uid.*", "outside the tree"),
    ("number.gid.*", "outside the tree"),
    ("number.mtime.*", "outside the tree"),
    ("number.devmajor.*", "outside the tree"),
    ("number.devminor.*", "outside the tree"),
    ("type.nul", "the typeflag NUL of regular files, from before POSIX"),
    ("v7.bytes-after-linkname", "bytes in fields that v7 headers do not use"),
    ("tree.dir-after-contents", "directories after their contents (to accept)"),
    ("tree.duplicate.dir-dir", "the same directory twice (to accept)"),
    ("pax.SCHILY.*", "vendor pax keys outside the tree"),
    ("pax.LIBARCHIVE.*", "vendor pax keys outside the tree"),
    ("pax.nul-in-value.SCHILY.xattr.*", "NUL in xattrs, which are outside the tree"),
    ("pax.nul-in-value.LIBARCHIVE.xattr.*", "NUL in xattrs, which are outside the tree"),
    ("pax.value-not-utf8.SCHILY.*",
     "binary values of vendor pax keys, such as xattrs, outside the tree"),
    ("pax.value-not-utf8.LIBARCHIVE.*",
     "binary values of vendor pax keys, such as xattrs, outside the tree"),
    ("pax.value-not-utf8.[acm]time", "outside the tree"),
    ("pax.value-not-utf8.[ug]id", "outside the tree"),
    ("pax.value-not-utf8.[ug]name", "outside the tree"),
]

# The default policy: the strict criteria that it lets through, and how; it rejects the others.
# A strict parser normalizes these names to the path they refer to, which is what tarscan.py
# compares to find duplicates, so normalizing hides none. The rest it accepts as they are, some
# only if condition() holds. Tarballs are pinned by their sha256, so one that ends early is
# caught before it is parsed.
DEFAULT = [
    ("name.leading-dot-slash", "normalize", "`./a` is `a`"),
    ("name.dot", "normalize", "`.` is the root of the tree"),
    ("name.dot-component", "normalize", "`a/./b` is `a/b`"),
    ("name.double-slash", "normalize", "`a//b` is `a/b`"),
    ("symlink.absolute", "accept", "created as it is: writing through a symlink is rejected"),
    ("end.missing", "accept", "the archive ends after a member, and its sha256 is pinned"),
    ("end.lone-zero-block", "accept", "the archive ends after a member, and its sha256 is pinned"),
    ("end.data-after", "accept", "ignored: a header there is `end.archive-after`, rejected"),
    ("pax-global.after-members", "accept", "if every global header has only a `comment`"),
    ("magic.posix-version-nuls", "accept", "as some Java archivers write it: `ustar\\0\\0\\0`"),
    ("pax.size-disagrees", "accept",
     "the pax size frames the member, as POSIX says: it is how sizes over 8 GiB are written"),
    ("pax.newline-in-value.SCHILY.xattr.*", "accept", "xattrs are not extracted"),
    ("pax.newline-in-value.LIBARCHIVE.xattr.*", "accept", "xattrs are not extracted"),
]

# Compressions that tarscan.py does not read: it scans these as uncompressed tar
UNREAD = (".tar.lz", ".tar.zst", ".tzst", ".tar.lzma", ".tlz", ".tar.Z")


def classify(feature):
    """("platform" | "allowed" | "strict" | "unclassified", category, description)"""
    if feature.startswith("platform."):
        return "platform", None, None
    for pattern, reason in ALLOWED:
        if fnmatch.fnmatchcase(feature, pattern):
            return "allowed", None, reason
    for pattern, category, description in STRICT:
        if fnmatch.fnmatchcase(feature, pattern):
            return "strict", category, description
    return "unclassified", None, None


def assessed(r):
    if "features" not in r:
        return False
    name = r.get("name") or r.get("url", "")
    return not (r.get("error") and r["compression"]["format"] == "none" and name.endswith(UNREAD))


def criterion(feature):
    """The criterion of a strict feature: a problem of number fields that shape the tree is one
    criterion for all of them, as a strict parser has one rule for it."""
    return re.sub(r"^number\.(size|mode|chksum)\.", "number.*.", feature)


def strict_features(r):
    found = {criterion(f) for f in r["features"] if classify(f)[0] == "strict"}
    if r.get("error") or r.get("compression_error") or r.get("compression", {}).get("truncated"):
        found.add("scan.error")
    return found


def default_rule(feature):
    """The rule of DEFAULT for a strict feature: (pattern, how, why), or None if rejected."""
    for rule in DEFAULT:
        if fnmatch.fnmatchcase(feature, rule[0]):
            return rule
    return None


def condition(feature, r):
    """Whether the conditions of DEFAULT hold for a feature that it accepts, from what the
    fingerprint of the tarball records about all of its headers."""
    fingerprint = r.get("fingerprint", {})
    if feature == "pax-global.after-members":
        return set(fingerprint.get("pax_global_keys", {})) <= {"comment"}
    return True


def default_rejects(r):
    """The strict features of a tarball that the default policy rejects."""
    return {f for f in strict_features(r) if not (default_rule(f) and condition(f, r))}


def may_have_25bfa32e6e71(r):
    """The features of UNREPORTED that a tarball that version 25bfa32e6e71 scanned may have: it
    reported what each of them implies, or recorded the pax keys and extended headers they need."""
    features, fingerprint = r["features"], r.get("fingerprint", {})
    pax, pax_global = fingerprint.get("pax_keys", {}), fingerprint.get("pax_global_keys", {})
    git = fingerprint.get("producer_hint", {}).get("git-archive", 0)
    may = {f"pax.value-not-utf8.{k}" for k in pax if k != "path"}
    # a comment that git archive wrote is a commit in hex
    may |= {f"pax-global.value-not-utf8.{k}" for k in pax_global
            if not (k == "comment" and git >= pax_global[k])}
    may |= {f + "-too-large" for f in features if f.endswith(".base256")}
    if "pax.empty-value" in features:
        may.add("pax.empty-value.*")
    if "pax-global.empty-value" in features:
        may.add("pax-global.empty-value.*")
    if "size" in pax:
        may |= {"pax.size-leading-zero", "pax.size-too-large"}
    if any("x" in s and ("L" in s or "K" in s) for s in fingerprint.get("extended_sequence", {})):
        may.add("extended.gnu-long-and-pax")
    return may


# Versions of tarscan.py that did not report some features: (those features, and a function of a
# tarball that version scanned to the ones it may have). A tarball that may have none of them is
# measured for them all the same; the others are not, until they are scanned again.
UNREPORTED = {
    "25bfa32e6e71": (
        ["pax.empty-value.*", "pax-global.empty-value.*", "pax.value-not-utf8.*",
         "pax-global.value-not-utf8.*", "pax.size-leading-zero", "pax.size-too-large",
         "extended.gnu-long-and-pax", "number.*.base256-too-large"],
        may_have_25bfa32e6e71,
    ),
}


@functools.cache
def overlap(a, b):
    """Whether two features, either of which may be a pattern, can be the same."""
    return fnmatch.fnmatchcase(a, b) or fnmatch.fnmatchcase(b, a)


def unreported(features, r):
    """Whether the version of tarscan.py that scanned a tarball did not report some of features."""
    return unreported_by(tuple(features), r.get("scanner"))


@functools.cache
def unreported_by(features, scanner):
    """Whether a version of tarscan.py did not report some of features: the same for every tarball
    it scanned, of which there are tens of thousands, and so remembered."""
    return any(overlap(f, u) for f in features for u in UNREPORTED.get(scanner, ([],))[0])


def unmeasured(r):
    """The features that a tarball may have, which the version of tarscan.py that scanned it did not
    report."""
    return UNREPORTED[r["scanner"]][1](r) if r.get("scanner") in UNREPORTED else set()


def unmeasured_criteria(r):
    """The strict criteria that may reject a tarball, unmeasured."""
    return {criterion(f) for f in unmeasured(r) if classify(f)[0] == "strict"}


def percent(n, total):
    return f"{100 * n / total:.2f}%" if total else "–"


def bound(total):
    """The 95% upper bound of a rate of which none of total were seen: the rule of three."""
    return f"<{300 / total:.2g}%" if total else "–"


def median_year(r):
    m = r.get("mtime")
    try:
        return time.gmtime(m[1]).tm_year if m else None
    except (OverflowError, OSError, ValueError):
        return None


def labels(names):
    """Datasets by their ecosystem, or by their directory where an ecosystem has several."""
    ecosystems = collections.Counter(n.split("/")[0] for n in names)
    return {n: n.split("/")[0] if ecosystems[n.split("/")[0]] == 1 else n for n in names}


def fixed_mtimes(rows):
    """mtimes that producers write in place of the real ones: those that all members of at least
    20 tarballs without a uname have, as producers that normalize mtimes also leave out names.
    Real dates, such as the commit that git archive writes, rarely repeat."""
    same = collections.Counter(
        r["mtime"][0]
        for r in rows
        if r.get("mtime")
        and r["mtime"][0] == r["mtime"][2]
        and set(r.get("fingerprint", {}).get("uname", {})) <= {""}
    )
    return {t for t, n in same.items() if n >= 20}


# The bins of mtime_bin: two years each, after the 1980s, then the tarballs it does not date
MTIME_BINS = ["1981–1989"] + [f"{y}–{y + 1}" for y in range(1990, 2027, 2)] + ["fixed", "unknown"]


def mtime_bin(r, fixed):
    """The bin of MTIME_BINS of a tarball by the median mtime of its members, "fixed" where all
    have one of fixed, and "unknown" where none is after 1980."""
    m = r.get("mtime")
    if m and m[0] == m[2] and m[0] in fixed and set(r["fingerprint"].get("uname", {})) <= {""}:
        return "fixed"
    y = median_year(r)
    if y is None or y <= 1980:
        return "unknown"
    if y < 1990:
        return "1981–1989"
    start = y - y % 2
    return f"{start}–{start + 1}"


def histogram(datasets, union):
    """Tarballs by the median mtime of their members, in bins of two years, for each dataset."""
    names = list(datasets)
    fixed = fixed_mtimes(union)
    bin_of = functools.partial(mtime_bin, fixed=fixed)

    counts = {name: collections.Counter() for name in names}
    total = collections.Counter()
    for name, rows in datasets.items():
        for r in rows:
            if "features" in r:
                counts[name][bin_of(r)] += 1
    for r in union:
        if "features" in r:
            total[bin_of(r)] += 1
    bins = [b for b in MTIME_BINS if total[b]]
    widest = max(total.values())
    columns = [labels(names)[n] for n in names] + ["all"]
    widths = [max(len(c), 5) for c in columns]
    lines = ["years      " + " ".join(f"{c:>{w}}" for c, w in zip(columns, widths))]
    for b in bins:
        bar = "#" * max(1, round(40 * total[b] / widest))
        cells = [counts[n][b] for n in names] + [total[b]]
        row = " ".join(f"{c:>{w}}" for c, w in zip(cells, widths))
        lines.append(f"{b:<10} {row}  {bar}")
    return "\n".join(lines), fixed


def scanned_section(datasets, names, short, rated, rows, union):
    """The ecosystems, and a histogram of when their tarballs were made."""
    lines = [
        "| ecosystem | tarballs | scanned | not assessed | latest | GB | members | origins |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for n in names:
        scanned = [r for r in datasets[n] if "features" in r]
        gb = sum(r.get("bytes") or 0 for r in scanned) / 1e9
        members = sum(r.get("members") or 0 for r in scanned)
        latest = sum(1 for r in rated[n] if r.get("latest"))
        origins = collections.Counter(origin(r["url"]) for r in scanned)
        top = ", ".join(f"{k} {v:,}" for k, v in origins.most_common(3))
        lines.append(
            f"| {short[n]} | {len(datasets[n])} | {len(scanned)} | "
            f"{len(scanned) - len(rated[n])} | {latest} | {gb:.1f} | {members:,} | {top} |"
        )
    gb = sum(r.get("bytes") or 0 for r in union) / 1e9
    scanned = sum(1 for r in rows if "features" in r)
    lines.append(
        f"| all, distinct | {len(rows)} | {scanned} | {scanned - len(union)} | "
        f"{sum(1 for r in union if r.get('latest'))} | {gb:.1f} | "
        f"{sum(r.get('members') or 0 for r in union):,} | |"
    )
    chart, fixed = histogram(datasets, rows)
    dates = ", ".join(time.strftime("%Y-%m-%d %H:%M", time.gmtime(t)) for t in sorted(fixed))
    return "\n".join(lines) + (
        "\n\nTarballs that are not scanned could not be downloaded from any URL. Not assessed: in "
        "a compression that the scanner does not read (`.tar.lz`, `.tar.zst`). Latest: the latest "
        "version of a package in its repository.\n\n"
        "Tarballs by the median mtime of their members, which dates most of them:\n\n"
        f"```\n{chart}\n```\n\n"
        "Fixed: every member has an mtime that a producer writes in place of the real one, such "
        "as `cabal sdist` (2001-09-09) on Hackage and hatchling (2020-02-02) on PyPI, so these "
        f"tarballs are not dated: {dates}. Unknown: no mtime after 1980."
    )


def passes(r):
    return not strict_features(r)


def passes_default(r):
    return not default_rejects(r)


def costliest(union, rejects=strict_features):
    """The criterion that rejects the most tarballs on its own."""
    sole = collections.Counter()
    for r in union:
        found = rejects(r)
        if len(found) == 1:
            sole[next(iter(found))] += 1
    return sole.most_common(1)[0][0] if sole else None


def headline(union):
    """What both policies reject of all tarballs together, as a sentence."""
    strict = sum(not passes(r) for r in union)
    default = sum(not passes_default(r) for r in union)
    return (
        f"**The default policy rejects {default} of {len(union):,} release tarballs "
        f"({percent(default, len(union))}); rejecting every criterion would reject {strict} "
        f"({percent(strict, len(union))}).** The criterion that rejects the most tarballs on its "
        f"own is `{costliest(union, default_rejects)}` of the default policy, and "
        f"`{costliest(union)}` of every criterion."
    )


def reject_table(names, short, rated, union):
    """Tarballs that each policy rejects, per ecosystem and of all of them."""
    lines = [
        "| ecosystem | tarballs | GB | rejected: every criterion | rejected: default policy |",
        "|---|---|---|---|---|",
    ]
    for n, rs in [(n, rated[n]) for n in names] + [(None, union)]:
        strict = sum(not passes(r) for r in rs)
        default = sum(not passes_default(r) for r in rs)
        cells = [
            short[n] if n else "**all, distinct**",
            f"{len(rs):,}",
            f"{sum(r.get('bytes') or 0 for r in rs) / 1e9:.1f}",
            f"{strict} ({percent(strict, len(rs))})",
            f"{default} ({percent(default, len(rs))})",
        ]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def readme(path, datasets, names, short, rated, rows, union):
    default = sum(not passes_default(r) for r in union)
    block = (
        f"Of the {len(union):,} source tarballs of {ecosystems(names)}, it "
        f"accepts {percent(len(union) - default, len(union))} ([per ecosystem]({SITE}#tarballs))."
    )
    text = open(path).read()
    begin, end = "<!-- begin strict.py -->", "<!-- end strict.py -->"
    head, rest = text.split(begin, 1)
    _, tail = rest.split(end, 1)
    with open(path, "w") as f:
        f.write(f"{head}{begin}{block}{end}{tail}")


def main():
    args = sys.argv[1:]
    readme_path = None
    if args[:1] == ["--readme"]:
        readme_path, args = args[1], args[2:]
    rows, datasets = load(args)
    names = list(datasets)
    short = labels(names)
    rated = {n: [r for r in datasets[n] if assessed(r)] for n in names}
    union = [r for r in rows if assessed(r)]
    if readme_path:
        readme(readme_path, datasets, names, short, rated, rows, union)
        return

    print("# Strict parsing of real tarballs\n")
    print(
        "How many release tarballs a strict tar parser rejects: with every criterion, each an "
        "ambiguity that [METHOD.md](../../METHOD.md) lists, and with the default policy. Generated "
        "by `contrib/scanner/strict.py` from the scans in this directory: see their `RUN.md` for "
        "how each was made.\n"
    )

    print("## What was scanned\n")
    print(scanned_section(datasets, names, short, rated, rows, union))

    print("\n## What each policy rejects\n")
    print(headline(union) + "\n")
    print(reject_table(names, short, rated, union))
    print()

    print("## The default policy\n")
    print(
        "The strict criteria that the default policy lets through, and how; it rejects all other "
        "criteria. Tarballs: of all ecosystems, with the feature where the policy lets it through.\n"
    )
    print("| criterion | how | why | tarballs |")
    print("|---|---|---|---|")
    for pattern, how, why in DEFAULT:
        count = sum(
            1 for r in union
            if any(fnmatch.fnmatchcase(f, pattern) and condition(f, r) for f in strict_features(r))
        )
        print(f"| `{pattern}` | {how} | {why} | {count} |")
    print()

    failing = collections.defaultdict(lambda: collections.defaultdict(list))
    for n in names:
        for r in rated[n]:
            for f in strict_features(r):
                failing[f][n].append(r)
    sole = collections.Counter()
    examples = collections.defaultdict(list)
    for r in union:
        found = strict_features(r)
        if len(found) == 1:
            sole[next(iter(found))] += 1
        for f in found:
            if len(examples[f]) < 3:
                name = f"{r['package']}@{r['version']}" if r["version"] else r["package"]
                examples[f].append(name)

    print("## Criteria\n")
    print(
        "Tarballs that each criterion rejects, per ecosystem. Default: what the default policy "
        "does with it. Alone: tarballs of all ecosystems that only this criterion rejects, which "
        "allowing it would let through.\n"
    )
    print(
        "| category | criterion | default | " + " | ".join(short[n] for n in names)
        + " | alone | examples |"
    )
    print("|---|---|---|" + "---|" * len(names) + "---|---|")
    order = sorted(
        failing,
        key=lambda f: (
            CATEGORIES.index(classify(f)[1]) if f != "scan.error" else 0,
            -sum(len(v) for v in failing[f].values()),
            f,
        ),
    )
    for f in order:
        category, description = ("framing", STRICT[0][2]) if f == "scan.error" else classify(f)[1:]
        cells = " | ".join(
            f"{len(failing[f][n])} ({percent(len(failing[f][n]), len(rated[n]))})"
            if failing[f][n]
            else "0"
            for n in names
        )
        rule = default_rule(f)
        print(
            f"| {category} | `{f}`: {description} | {rule[1] if rule else 'reject'} | {cells} | "
            f"{sole[f]} | {', '.join(examples[f])} |"
        )
    print()
    print(
        "Other criteria reject no tarball here. That is no proof that they cost nothing: with 95% "
        "confidence, each rejects less than "
        + ", ".join(f"{bound(len(rated[n]))[1:]} of {short[n]}" for n in names)
        + ".\n"
    )

    print("## Not measured\n")
    old = [r for r in union if r.get("scanner") in UNREPORTED]
    if not old:
        print("Every tarball was scanned by a version of `tarscan.py` that reports every feature.\n")
    else:
        versions = collections.Counter(r["scanner"] for r in old)
        print(
            f"Of the {len(union):,} tarballs, "
            + "; ".join(f"{k:,} were scanned by `{v}`, a version of `tarscan.py` that did not "
                        "report " + ", ".join(f"`{f}`" for f in UNREPORTED[v][0])
                        for v, k in versions.most_common())
            + f"; the other {len(union) - len(old):,} were scanned by a later version. What the "
            "earlier versions did record rules out most of these features: a tarball without a "
            "pax `size` has no pax size with a leading zero. `UNREPORTED` in "
            "`contrib/scanner/strict.py` says how, for each version.\n"
        )
        missing = collections.Counter(f for r in old for f in unmeasured_criteria(r))
        if missing:
            print(
                "It does not rule out all strict criteria. These are not measured in some "
                "tarballs, which they may reject, more than the tables above say:\n"
            )
            print("| criterion | tarballs not measured |")
            print("|---|---|")
            for f, count in missing.most_common():
                print(f"| `{f}` | {count} |")
            print()
        else:
            print("It rules out every strict criterion for every one of them, so the tables "
                  "above measure every tarball.", end="")
        allowed = collections.Counter(
            f for r in old for f in unmeasured(r) if classify(f)[0] == "allowed")
        if allowed:
            print(
                ("" if missing else " ")
                + "It does not rule out these allowed features, in fields outside the tree, which "
                "the table below counts only where they were reported: "
                + ", ".join(f"`{f}` in {c:,}" for f, c in allowed.most_common()) + ".",
                end="",
            )
        print("\n")

    print("## Allowed features\n")
    print("Not ambiguous, or confined to fields outside the tree. Tarballs of all ecosystems:\n")
    print("| feature | why it is allowed | tarballs |")
    print("|---|---|---|")
    allowed = collections.Counter(
        f for r in union for f in r["features"] if classify(f)[0] == "allowed"
    )
    for f, count in allowed.most_common():
        print(f"| `{f}` | {classify(f)[2]} | {count} |")
    print()
    platform = collections.Counter(
        f for r in union for f in r["features"] if classify(f)[0] == "platform"
    )
    if platform:
        print(
            "Names that some filesystems cannot hold, so that extraction fails there only: "
            + ", ".join(f"`{f}` {c}" for f, c in platform.most_common())
            + ".\n"
        )
    unclassified = collections.Counter(
        f for r in union for f in r["features"] if classify(f)[0] == "unclassified"
    )
    if unclassified:
        print("## Unclassified features\n")
        print("Neither strict nor allowed yet: " + ", ".join(
            f"`{f}` {c}" for f, c in unclassified.most_common()) + ".\n")


if __name__ == "__main__":
    with contextlib.redirect_stdout(io.StringIO()) as out:
        main()
    print(tidy_tables(out.getvalue()), end="")

"""Write the site of the test suite, as static files: a page per case, named by its identifier, and an index.

    python -I contrib/site.py docs contrib/data/*/*/results.jsonl

Every page is generated, from what the rest of the repository has: the case's script and archive,
what implementations make of it (matrix/matrix.json), and how many source tarballs have
its feature, of which the default policy of scanner/strict.py rejects how many. Static HTML with a
stylesheet, and no scripts: the SVGs are part of the pages, so that their hover titles and the
links of the matrix work.
"""

import collections
import datetime
import hashlib
import html
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "matrix"))
sys.path.insert(0, os.path.join(HERE, "scanner"))
import matrix  # noqa: E402
import strict  # noqa: E402
import tarscan  # noqa: E402
from report import ecosystems, load  # noqa: E402

REPO = "https://github.com/haampie/tar-minefield"
# The DOI of every version on Zenodo, as CITATION.cff has it
with open(os.path.join(os.path.dirname(HERE), "CITATION.cff")) as f:
    DOI = re.search(r"^doi: (\S+)$", f.read(), re.M).group(1)
CASES = os.path.join(matrix.ROOT, "suite", "cases")
# The verdict at the top of a case's page: its badge, and what it requires, which for cases with a
# tree ends with it
VERDICTS = {
    "accept": ("Must accept", "Every implementation must accept this archive, and extract this tree: "),
    "tolerate": ("Tolerated", "A strict parser may reject this archive. If it accepts it, it must "
                 "extract this tree: "),
    "reject": ("Must reject", "A strict parser must reject this archive: implementations disagree on "
               "its tree."),
}
# Identifiers that a case no longer has, and the one it has now: the pages of the old ones redirect
MOVED = {"G01": "F17", "G02": "F18", "G03": "F19", "G04": "N21"}
OUTCOMES = {
    "✅": "as the verdict says",
    "⚠️": "accepts",
    "⛔": "rejects",
    "❌": "another tree, or rejects",
    "💥": "writes outside the destination",
    "❔": "not run, so not verified",
}
# Tables of one kind have the same columns, in the same widths
COLUMNS = {
    "cases": [("identifier", 14), ("name", 24), ("what it is", 48), ("prevalence", 14, "n")],
    "data": [("ecosystem", 25), ("tarballs", 25, "n"), ("with it", 25, "n"), ("share", 25, "n")],
    "data-policy": [("ecosystem", 20), ("tarballs", 20, "n"), ("with it", 20, "n"),
                    ("share", 20, "n"), ("rejected by the default policy", 20, "n")],
    "tarballs": [("ecosystem", 25), ("tarballs", 25, "n"), ("rejected", 25, "n"), ("share", 25, "n")],
    "reasons": [("why", 80), ("tarballs", 20, "n")],
    "examples": [("case", 8), ("the archive", 36), ("what implementations make of it", 56)],
    "seen": [("tarball", 55), ("packaged by", 12), ("example from the tarball", 33)],
    "implementations": [("implementation", 21), ("version", 21), ("outcome", 18),
                        ("what it makes of it", 40)],
}
STYLE = """\
body { max-width: 66rem; margin: 0 auto; padding: 1rem; font: 16px/1.5 system-ui, sans-serif;
       color: #1f2328; background: #ffffff; }
a { color: #0969da; }
code, pre { font: 0.875em ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }
pre { background: #f6f8fa; padding: 0.75rem; overflow-x: auto; }
code { background: #e8ebef; padding: 0.1em 0.3em; border-radius: 4px; }
pre code { background: none; padding: 0; }
table { border-collapse: collapse; margin: 1rem 0; width: 100%; table-layout: fixed; }
th, td { border: 1px solid #d0d7de; padding: 0.25rem 0.5rem; text-align: left;
         vertical-align: baseline; overflow-wrap: anywhere; }
th { background: #f6f8fa; }
td.n, th.n { text-align: right; font-variant-numeric: tabular-nums; }
svg { max-width: 100%; height: auto; }
.wide { overflow-x: auto; }
/* A table is not narrower than this: on a narrow screen it scrolls, rather than squeezing words */
.wide > table { min-width: 40rem; }
dt { font-weight: 600; }
.note { color: #59636e; font-size: 0.875em; }
/* The footer, muted, of three items with a dot between them */
footer { color: #59636e; font-size: 0.875em; }
footer a { color: inherit; }
footer .sep { margin: 0 0.5rem; }
/* The DOI, as a badge like Zenodo's, of text rather than an image of another site: inline, so
   that its text is on the line of the text around it */
a.doi { font-size: 0.75em; text-decoration: none; white-space: nowrap; }
a.doi span { padding: 0.125em 0.375rem; color: #ffffff; }
a.doi span:first-child { background: #555555; border-radius: 3px 0 0 3px; }
a.doi span + span { background: #0969da; border-radius: 0 3px 3px 0; }
/* Previous, the index and next in columns that do not move: names that do not fit end in … */
nav { display: grid; grid-template-columns: minmax(0, 1fr) auto minmax(0, 1fr); gap: 1rem; }
nav a { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
nav .next { text-align: right; }
/* The link to a section, next to its heading when it is hovered */
.anchor { margin-left: 0.375rem; color: #8c959f; text-decoration: none; visibility: hidden; }
h2:hover .anchor, h3:hover .anchor, .anchor:focus { visibility: visible; }
/* The files of a case: its name as the link, what it is beside it, and the archive's sha256 under
   that, muted and without the background of code */
table.files { width: auto; table-layout: auto; margin: 0; }
table.files td { border: 0; padding: 0 1rem 0.125rem 0; }
table.files code { background: none; padding: 0; }
table.files td:first-child { white-space: nowrap; }
@media (max-width: 40rem) {
  /* the matrix and the block maps at their size, scrolled, rather than too small to read */
  .wide svg { max-width: none; }
  dd { margin-left: 1rem; }
  table.files, table.files tr, table.files td { display: block; }
  table.files td + td { padding: 0 0 0.375rem 1rem; }
  /* the tarballs of seen-in.html, the implementations of a case and the motivating examples,
     one block per row */
  table.seen, table.seen tr, table.seen td,
  table.implementations, table.implementations tr, table.implementations td,
  table.examples, table.examples tr, table.examples td { display: block; }
  table.seen colgroup, table.seen th, table.implementations colgroup, table.implementations th,
  table.examples colgroup, table.examples th { display: none; }
  table.seen tr, table.implementations tr, table.examples tr { margin-bottom: 0.5rem;
                                                                border: 1px solid #d0d7de; }
  table.seen td, table.implementations td, table.examples td { border: 0; }
  .wide > table.seen, .wide > table.implementations, .wide > table.examples { min-width: 0; }
  table.examples td:first-child { font-weight: 600; }
  table.seen td:nth-child(2):not(:empty)::before { content: "packaged by "; color: #59636e; }
  table.implementations td:first-child { font-weight: 600; }
  table.implementations td:nth-child(2) { color: #59636e; font-size: 0.875em; }
}
/* A sha256: its label, then the hash, which a click selects whole, wherever it wraps */
.hash { display: block; color: #59636e; font-size: 0.8125em; }
.hash code { background: none; padding: 0; word-break: break-all; -webkit-user-select: all;
             user-select: all; }
/* The verdict of a case, as a solid badge and in words: unlike the pale cells of the matrix, whose
   colours are outcomes */
.verdict { margin: 1rem 0; padding: 0.5rem 1rem; background: #f6f8fa; border-left: 6px solid;
           overflow-wrap: anywhere; }
.verdict p { margin: 0.25rem 0; }
.badge { display: inline-block; margin-right: 0.5rem; padding: 0 0.5rem; border-radius: 4px;
         color: #ffffff; font-weight: 700; }
.accept { border-color: #1a7f37; } .accept .badge { background: #1a7f37; }
.reject { border-color: #cf222e; } .reject .badge { background: #cf222e; }
.tolerate { border-color: #59636e; } .tolerate .badge { background: #59636e; }
"""


# The stylesheet by its contents, so that browsers do not keep an old one
STYLE_VERSION = hashlib.sha256(STYLE.encode()).hexdigest()[:8]


def prevalence(k, n):
    """A share of tarballs with two decimals, so that a right-aligned column lines up on the
    point; one that would round to 0 says so."""
    return "&lt;0.01%" if 0 < 10000 * k < n else f"{100 * k / n:.2f}%"


# The footnote of the index for a prevalence marked with *
UNMEASURED = ('<p class="note" id="unmeasured">* Not measured in some tarballs, which an earlier '
              "version of <code>tarscan.py</code> scanned: it did not report this, and what it did "
              "record does not rule it out. The case's page says how many.</p>")


def unmeasured(features, rows):
    """The tarballs of rows that may have one of features, which the version of tarscan.py that
    scanned them did not report, and what else it recorded does not rule out."""
    scanners = unreported_by(features)
    if not scanners:
        return []
    return [r for r in rows if r.get("scanner") in scanners
            and any(strict.overlap(f, u) for f in features for u in strict.unmeasured(r))]


def unreported_by(features):
    """The versions of tarscan.py that did not report some of features: for most, none."""
    return {v for v in strict.UNREPORTED if strict.unreported_by(tuple(features), v)}


def table(kind, rows):
    """A table of a kind of COLUMNS, with rows of HTML."""
    columns = COLUMNS[kind]
    cols = "".join(f'<col style="width: {c[1]}%">' for c in columns)
    head = "".join(f"<th class=n>{c[0]}</th>" if c[2:] else f"<th>{c[0]}</th>" for c in columns)
    return (f'<div class="wide"><table class="{kind}"><colgroup>{cols}</colgroup><tr>{head}</tr>\n'
            + "\n".join(rows) + "</table></div>")


def markdown(p):
    """A line of the README as HTML: code, bold, italics and links. Links into the repository go
    to GitHub, and links to the site to its pages."""

    def href(url):
        if url.startswith(matrix.SITE.rstrip("/")):
            return url[len(matrix.SITE):] or "index.html"
        if url.startswith("#"):
            return f"{REPO}{url}"
        return url if re.match(r"https?:", url) else f"{REPO}/blob/main/{url}"

    out = []
    for i, part in enumerate(p.split("`")):
        if i % 2:
            out.append(f"<code>{html.escape(part)}</code>")
            continue
        part = html.escape(part, quote=False)
        part = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", part)
        part = re.sub(r"\*(.+?)\*", r"<em>\1</em>", part)
        out.append(re.sub(r"\[(.+?)\]\((.+?)\)", lambda m: f'<a href="{href(m.group(2))}">'
                          f"{m.group(1)}</a>", part))
    return "".join(out)


def readme():
    with open(os.path.join(matrix.ROOT, "README.md")) as f:
        return re.sub(r"<!-- (begin|end) \S+ -->\n?", "", f.read())


def readme_intro():
    """The introduction of the README, between its title and its first section, as HTML: so that
    the site says what the README says."""
    text = readme().split("\n## ", 1)[0].split("\n", 1)[1]
    # badges, such as the DOI's, are for GitHub: they are images of other sites
    return "\n".join(f"<p>{markdown(' '.join(p.split()))}</p>"
                     for p in text.strip().split("\n\n") if not p.startswith("[!["))


def readme_examples():
    """The table of the README's motivating examples, as HTML."""
    section = readme().split("\n## Motivating examples\n", 1)[1].split("\n## ", 1)[0]
    lines = [line.strip().strip("|") for line in section.splitlines() if line.startswith("|")]
    rows = ["<tr>" + "".join(f"<td>{markdown(c.strip())}</td>" for c in line.split(" | ")) + "</tr>"
            for line in lines[2:]]
    return table("examples", rows)


def readme_section(title):
    """A section of the README of paragraphs and lists, as HTML."""
    section = readme().split(f"\n## {title}\n", 1)[1].split("\n## ", 1)[0]
    blocks = []
    for block in section.strip().split("\n\n"):
        lines = block.splitlines()
        if all(line.startswith("- ") for line in lines):
            blocks.append("<ul>\n" + "\n".join(f"<li>{markdown(line[2:])}</li>" for line in lines)
                          + "\n</ul>")
        else:
            blocks.append(f"<p>{markdown(' '.join(block.split()))}</p>")
    return "\n".join(blocks)


def inline(text):
    """Text with `code` as HTML."""
    parts = text.split("`")
    return "".join(f"<code>{html.escape(p)}</code>" if i % 2 else html.escape(p)
                   for i, p in enumerate(parts))


def paragraphs(text):
    out = []
    text = re.sub(r"\n(Decision point|Seen in):", r"\n\n\1:", text.strip())
    for p in text.split("\n\n"):
        p = inline(" ".join(p.strip().split("\n")))
        out.append("<p>" + re.sub(r"^(Decision point|Seen in):", r"<strong>\1:</strong>", p)
                   + "</p>")
    return "\n".join(out)


TITLE = "Tar file extraction test suite"
# How many tarballs seen-in.html lists as examples of a case whose tarballs are accepted
EXAMPLES = 8


def anchored(body):
    """Every heading of a section with an id, its own or one made of its text, and a link to it
    that shows when the heading is hovered, so that a section can be linked to."""
    ids = set(re.findall(r'id="([^"]+)"', body))

    def heading(m):
        tag, attrs, text = m.groups()
        own = re.search(r'id="([^"]+)"', attrs)
        if own:
            anchor = own.group(1)
        else:
            words = html.unescape(re.sub(r"<[^>]+>", "", text)).lower()
            base = re.sub(r"[^a-z0-9]+", "-", words).strip("-")
            anchor, n = base or "section", 1
            while anchor in ids:
                n += 1
                anchor = f"{base}-{n}"
            ids.add(anchor)
            attrs += f' id="{anchor}"'
        return (f'<{tag}{attrs}>{text}<a class="anchor" href="#{anchor}" '
                f'aria-label="Link to this section">¶</a></{tag}>')

    return re.sub(r"<(h[23])((?: [^>]*)?)>(.*?)</\1>", heading, body, flags=re.S)


def page(title, description, body):
    body = anchored(body)
    return (
        '<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        f"<title>{html.escape(title)}</title>\n"
        f'<meta name="description" content="{html.escape(description)}">\n'
        f'<link rel="stylesheet" href="style.css?{STYLE_VERSION}">\n</head>\n<body>\n'
        f"{body}\n<hr>\n<footer>Generated by <code>contrib/site.py</code> of "
        f'<a href="{REPO}">tar-minefield</a><span class="sep">·</span>Last updated {UPDATED}'
        f'<span class="sep">·</span><a class="doi" href="https://doi.org/{DOI}"><span>DOI</span>'
        f"<span>{DOI}</span></a></footer>\n</body>\n</html>\n"
    )


# Where the footer of a page says when it last changed, which main() fills in
UPDATED = "<!-- updated -->"
DATE = re.compile(r'<time datetime="[0-9-]+">[0-9-]+</time>')


def dated(text, old):
    """A page with the date it last changed: that of its old version, if the page is the same apart
    from the date, so that generating the site again changes nothing; or else today, in UTC."""
    if old is not None and DATE.sub(UPDATED, old, count=1) == text:
        return old
    today = datetime.datetime.now(datetime.timezone.utc).date().isoformat()
    return text.replace(UPDATED, f'<time datetime="{today}">{today}</time>')


def hexdump(data):
    """Bytes as `xxd` writes them, so that `xxd -r` makes them again."""
    lines = []
    for i in range(0, len(data), 16):
        row = data[i : i + 16]
        hexes = " ".join(row[j : j + 2].hex() for j in range(0, len(row), 2))
        text = "".join(chr(b) if 32 <= b < 127 else "." for b in row)
        lines.append(f"{i:08x}: {hexes:<39}  {text}")
    return "\n".join(lines) + "\n"


def error_line(error):
    """An error on one line, shortened, with control characters such as a NUL escaped."""
    line = "".join(c if c.isprintable() else f"\\x{ord(c):02x}" for c in " ".join(error.split()))
    return line if len(line) <= 200 else line[:199] + "…"


def features_of(case, info):
    """The features a case is about: those of its script, or for cases to accept, which have none
    to reject, the allowed features that tarscan.py reports of it."""
    if info["features"]:
        return info["features"]
    with open(os.path.join(matrix.ARCHIVES, case + ".tar"), "rb") as f:
        r = tarscan.scan(io.BytesIO(f.read()))
    return [f for f in r["features"] if strict.classify(f)[0] == "allowed"]


def policy(info, features):
    """What the default policy does with a case, as HTML."""
    if info["verdict"] == "reject":
        return "rejects it"
    if info["verdict"] == "accept":
        reasons = [f"<code>{f}</code>: {inline(strict.classify(f)[2])}" for f in features]
        return "accepts it" + (", as it allows " + "; ".join(reasons) if reasons else "")
    rules = [strict.default_rule(f) for f in features]
    return "; ".join(f"{how}s <code>{html.escape(f)}</code>: {inline(why)}"
                     for f, (_, how, why) in zip(features, rules))


def data_section(ident, features, names, short, rated, union):
    """How many tarballs of each ecosystem have the features, and what the default policy does
    with them: a sentence where it rejects all or none of them for the features, and a column
    where it rejects some. seen-in.html lists them: all that it rejects, or else examples."""
    if not features:
        return "<p>This case is not measured in source tarballs on its own.</p>"

    def has(r):
        return any(f in r["features"] for f in features)

    def rejected(r):
        return any(strict.criterion(f) in strict.default_rejects(r) for f in features)

    counts = []
    for n, rs in [(short[n], rated[n]) for n in names] + [("all, distinct", union)]:
        with_it = [r for r in rs if has(r)]
        counts.append((n, len(rs), len(with_it), sum(rejected(r) for r in with_it),
                       len(unmeasured(features, rs))))
    _, _, k, j, u = counts[-1]
    mixed = 0 < j < k
    rows = []
    for n, total, k, j, un in counts:
        cells = [html.escape(n), f"{total:,}", f"{k:,}" + ("*" if un else ""),
                 prevalence(k, total) + ("*" if un else "")]
        cells += [str(j)] if mixed else []
        rows.append("<tr><td>" + "</td><td class=n>".join(cells) + "</td></tr>")
    policy = ("" if not k else " The default policy rejects some of them, as the last column "
              "says, and accepts the others." if mixed else " The default policy rejects all of "
              "them." if j else " The default policy accepts them.")
    scanners = unreported_by(features)
    old = sum(1 for r in union if r.get("scanner") in scanners) if scanners else 0
    note = (f'<p class="note">* Not measured in {u:,} tarballs, which an earlier version of '
            "<code>tarscan.py</code> scanned: it did not report this, and what it did record does "
            "not rule it out. They are counted as not having it, so the share may be higher.</p>\n"
            if u else
            f'<p class="note">{old:,} of these tarballs were scanned by an earlier version of '
            "<code>tarscan.py</code>, which did not report this. What it did record rules it out "
            'for all of them: see <a href="' + REPO + '/blob/main/contrib/data/STRICT.md#not-measured">'
            "STRICT.md</a>.</p>\n" if old else "")
    return (
        f"<p>Release tarballs of {ecosystems(names)} with "
        + ", ".join(f"<code>{f}</code>" for f in features) + "." + policy + "</p>\n"
        + table("data-policy" if mixed else "data", rows) + "\n" + note
        + ("" if not k else f'<p>See <a href="seen-in.html#{ident}">'
           + (f"the list of the {j:,} it rejects" if mixed
              else f"the list of these {k:,} tarballs" if j or k <= EXAMPLES
              else f"a sample of these {k:,} tarballs")
           + "</a>, with the sha256 of each and an example from it.</p>")
    )


def implementations_section(case, info, results):
    names = matrix.columns(results)
    versions = {i["name"]: i["version"] for i in results["implementations"]}
    cells, letters = matrix.case_cells(info, results["cases"].get(case, {}), names)
    trees = {v: k for k, v in letters.items()}
    rows = []
    for n in names:
        r = results["cases"].get(case, {}).get(n)
        symbol = next(s for s in matrix.ORDER if cells[n].startswith(s))
        letter = cells[n][len(symbol):].lstrip("️")
        if r is None:
            what = "not installed where this case was run"
        elif r["outside"]:
            what = "writes outside: " + inline(matrix.describe(r["outside"]))
        elif r["error"] == "rejected":
            what = "rejects it"
        elif r["error"]:
            what = "error: " + html.escape(error_line(r["error"]))
        elif letter:
            what = f"tree {letter}: " + inline(trees[letter])
        else:
            what = "the tree of the case" if info["verdict"] != "reject" else ""
        rows.append(f"<tr><td>{html.escape(n)}</td><td>{html.escape(versions.get(n, ''))}</td>"
                    f"<td>{symbol} {OUTCOMES[symbol]}</td><td>{what}</td></tr>")
    return table("implementations", rows)


def verdict(info):
    """The verdict of a case, as a banner: what it requires, with the tree unless it is to reject."""
    v = info["verdict"]
    badge, text = VERDICTS[v]
    if v != "reject":
        text = html.escape(text) + inline(matrix.describe(matrix.expected_tree(info))) + "."
    else:
        text = html.escape(text)
    return f'<div class="verdict {v}"><p><span class="badge">{badge}</span> {text}</p></div>'


def case_page(case, info, results, data):
    ident, name = matrix.label(case, info).split(" ", 1)
    with open(os.path.join(CASES, case + ".py")) as f:
        doc = f.read().split('"""')[1]
    with open(os.path.join(matrix.ARCHIVES, case + ".svg")) as f:
        block_map = f.read()
    with open(os.path.join(matrix.ARCHIVES, case + ".txt")) as f:
        dump = f.read()
    with open(os.path.join(matrix.ARCHIVES, case + ".tar"), "rb") as f:
        archive = f.read()
    features = features_of(case, info)
    category = strict.CATEGORIES["FNKS".index(ident[0])]
    files = f"{REPO}/blob/main/suite"
    body = f"""<h1><code>{ident}</code> {html.escape(name)}</h1>
<p>{inline(info["description"])}</p>
{verdict(info)}
<dl>
<dt>Category</dt><dd>{html.escape(category)}</dd>
<dt>Default policy</dt><dd>{policy(info, features)}</dd>
<dt>Files</dt><dd><table class="files">
<tr><td><a href="{REPO}/raw/main/suite/archives/{case}.tar"><code>{case}.tar</code></a></td>
<td>test archive, {len(archive):,} bytes
<span class="hash">sha256 <code>{hashlib.sha256(archive).hexdigest()}</code></span></td></tr>
<tr><td><a href="{files}/archives/{case}.json"><code>{case}.json</code></a></td><td>expected result</td></tr>
<tr><td><a href="{files}/archives/{case}.txt"><code>{case}.txt</code></a></td><td>annotated blocks</td></tr>
<tr><td><a href="{files}/cases/{case}.py"><code>{case}.py</code></a></td><td>generator script</td></tr>
</table></dd>
</dl>
<h2>The case</h2>
{paragraphs(doc.strip().split(chr(10), 1)[1])}
<h2>The archive</h2>
<p>Every block of 512 bytes, to scale, with its offset. Hover over a field for its bytes.</p>
<div class="wide">{block_map}</div>
<details><summary>Every block, as text</summary>
<pre>{html.escape(dump)}</pre>
</details>
<details><summary>Every byte, as a hex dump</summary>
<p>As <code>xxd</code> writes it: <code>xxd -r</code> makes the archive of it.</p>
<pre>{html.escape(hexdump(archive))}</pre>
</details>
"""
    body += ("<h2>What implementations make of it</h2>\n"
             + implementations_section(case, info, results) + "\n")
    body += "<h2>Prevalence in source tarballs</h2>\n" + data_section(ident, features, *data) + "\n"
    return page(f"{ident} {name} · {TITLE}", info["description"].replace("`", ""), body)


def seen_in_problems(cases, union):
    """Cases whose `Seen in:`, which is written by hand, contradicts the scans: no tarball where
    the scans have some, or tarballs where they have none."""
    problems = []
    for case, info in cases.items():
        with open(os.path.join(CASES, case + ".py")) as f:
            seen = re.search(r"^Seen in: *(.*)", f.read().split('"""')[1], re.M)
        features = features_of(case, info)
        if not seen or not features:
            continue
        k = sum(1 for r in union if any(f in r["features"] for f in features))
        none = seen.group(1).startswith("no source tarball")
        if none and k or not none and not k:
            problems.append(f"{case}: Seen in: {seen.group(1)!r}, but {k} tarballs have "
                            f"{', '.join(features)}")
    return problems


def mtimes_svg(union):
    """A bar chart of the tarballs by the median mtime of their members, in the bins of
    strict.MTIME_BINS that date them, and the numbers of those it leaves out: fixed and unknown."""
    fixed = strict.fixed_mtimes(union)
    counts = collections.Counter(strict.mtime_bin(r, fixed) for r in union)
    bins = [b for b in strict.MTIME_BINS if b not in ("fixed", "unknown")]
    width, height, left, top, bottom, gap = 640, 240, 48, 12, 28, 2
    step = (width - left) / len(bins)
    most = max(counts[b] for b in bins)
    # gridlines at a round step, of 1, 2 or 5 times a power of ten, at most six of them
    tick = next(m * 10**e for e in range(9) for m in (1, 2, 5) if most / (m * 10**e) <= 6)
    peak = -(-most // tick) * tick
    scale = (height - top - bottom) / peak
    base = height - bottom
    out = []
    for t in range(0, peak + 1, tick):
        y = base - t * scale
        out.append(f'<line x1="{left}" x2="{width}" y1="{y:.1f}" y2="{y:.1f}" class="grid"/>'
                   f'<text x="{left - 6}" y="{y + 4:.1f}" text-anchor="end">{t:,}</text>')
    for i, b in enumerate(bins):
        x, w, h = left + i * step + gap / 2, step - gap, counts[b] * scale
        r = min(4, w / 2, h)
        # rounded at the top, square on the baseline
        out.append(f'<path d="M{x:.1f},{base}v{-(h - r):.1f}q0,{-r:.1f} {r:.1f},{-r:.1f}'
                   f'h{w - 2 * r:.1f}q{r:.1f},0 {r:.1f},{r:.1f}v{h - r:.1f}z">'
                   f"<title>{b}: {counts[b]:,} tarballs</title></path>")
        start = b.split("–")[0]
        if start.endswith("0"):
            # a decade at the left edge of its first bin
            edge = left + i * step
            out.append(f'<line x1="{edge:.1f}" x2="{edge:.1f}" y1="{base}" y2="{base + 5}" class="grid"/>'
                       f'<text x="{edge:.1f}" y="{base + 18}" text-anchor="middle">{start}</text>')
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" '
           f'height="{height}" role="img"><title>Tarballs by the median mtime of their members, in '
           "bins of two years</title><style>text { font: 12px system-ui, sans-serif; fill: #59636e; } "
           "path { fill: #0969da; } path:hover { fill: #0550ae; } "
           ".grid { stroke: #d0d7de; stroke-width: 1; }</style>" + "".join(out) + "</svg>")
    return svg, counts["fixed"], counts["unknown"]


def tarballs_section(names, short, rated, union):
    """What the default policy rejects of the source tarballs, per ecosystem."""
    rows = []
    for n, rs in [(short[n], rated[n]) for n in names] + [("all, distinct", union)]:
        j = sum(not strict.passes_default(r) for r in rs)
        rows.append(f"<tr><td>{html.escape(n)}</td><td class=n>{len(rs):,}</td>"
                    f"<td class=n>{j:,}</td><td class=n>{prevalence(j, len(rs))}</td></tr>")
    rejected = sum(not strict.passes_default(r) for r in union)
    accepted = strict.percent(len(union) - rejected, len(union))
    svg, fixed, unknown = mtimes_svg(union)
    return (f'<h2 id="tarballs">Data to support the default policy</h2>\n<p>The default policy accepts '
            f"{accepted} of the {len(union):,} distinct release tarballs of {ecosystems(names)}. "
            f'See <a href="seen-in.html#rejected">the list of the {rejected:,} it rejects</a>, '
            "and why.</p>\n"
            + table("tarballs", rows)
            + f"<p>The tarballs by the median mtime of their members, a rough check that the data "
            f"spans enough years, leaving out the {fixed + unknown:,} whose mtimes are fixed for "
            f"reproducibility or missing:</p>\n"
            f'<div class="wide">{svg}</div>\n')


def printable(name):
    """A path as it can be shown: bytes that are not UTF-8 and control characters escaped."""
    name = name.encode("utf-8", "surrogateescape").decode("utf-8", "backslashreplace")
    return "".join(c if c.isprintable() else f"\\x{ord(c):02x}" for c in name)


def seen_row(r, short, example, also=""):
    """A source tarball: its name, as a link to where it was downloaded from, with its sha256; the
    ecosystems that package it; and an example from it."""
    name = f"{r['package']} {r['version']}" if r["version"] else r["package"]
    ecosystems = ", ".join(short[n] for n in r["datasets"] if n in short)
    example = f"<code>{html.escape(printable(example))}</code>" if example else ""
    return (f'<tr><td><a href="{html.escape(r["url"])}" rel="nofollow">{html.escape(name)}</a>'
            f'<span class="hash">sha256 <code>{r["sha256"]}</code></span></td>'
            f"<td>{html.escape(ecosystems)}</td>"
            f"<td>{example}{also}</td></tr>")


def seen_page(cases, data):
    """The source tarballs that cases are seen in: every one that the default policy rejects, by
    why, under the cases of the criterion where there are some; and for the other cases, examples
    of tarballs that have their feature. Each listed with an example from the tarball where the
    scan recorded one."""
    names, short, rated, union = data
    by_criterion = {}
    for case, info in cases.items():
        for f in info["features"]:
            by_criterion.setdefault(strict.criterion(f), []).append(info["id"])

    def what(criterion):
        """The reason of a criterion, which criteria with the same description share."""
        if criterion == "scan.error":
            return "an archive that could not be read past a header"
        return strict.classify(criterion)[2] or criterion

    rejected = sorted((r for r in union if not strict.passes_default(r)),
                      key=lambda r: (r["package"].lower(), r["version"] or ""))
    reasons = {r["sha256"]: {} for r in rejected}  # {reason: example or None}, per tarball
    ids = collections.defaultdict(set)
    criteria = {}  # the first criterion of a reason, which names its section
    for r in rejected:
        for c in sorted(strict.default_rejects(r)):
            example = next((e[0] for f, e in (r.get("examples") or {}).items()
                            if strict.criterion(f) == c and e), None)
            reasons[r["sha256"]].setdefault(what(c), example)
            ids[what(c)].update(by_criterion.get(c, []))
            criteria.setdefault(what(c), c)
    counts = collections.Counter(w for rs in reasons.values() for w in rs)

    def anchor(w):
        return "why-" + re.sub(r"[^a-z0-9]+", "-", criteria[w].lower()).strip("-")

    def cases_of(w):
        links = ", ".join(f'<a href="{i}.html">{i}</a>' for i in sorted(ids[w]))
        return f" ({links})" if links else ""

    summary = [f'<tr><td><a href="#{anchor(w)}">{inline(w)}</a>{cases_of(w)}</td><td class=n>{k}</td></tr>'
               for w, k in counts.most_common()]
    sections, anchored = [], set()
    for w, k in counts.most_common():
        # a case's anchor is on the first section of its criteria
        spans = "".join(f'<span id="{i}"></span>' for i in sorted(ids[w] - anchored))
        anchored |= ids[w]
        rows = []
        for r in rejected:
            if w in reasons[r["sha256"]]:
                others = [o for o in reasons[r["sha256"]] if o != w]
                also = ("<br>also: " + "; ".join(f'<a href="#{anchor(o)}">{inline(o)}</a>' for o in others)
                        if others else "")
                rows.append(seen_row(r, short, reasons[r["sha256"]][w], also))
        sections.append(f'<h3 id="{anchor(w)}">{spans}{inline(w[:1].upper() + w[1:])}'
                        f"{cases_of(w)}: {k}</h3>\n" + table("seen", rows))
    examples = []
    for case, info in cases.items():
        features = features_of(case, info)
        has = [r for r in union if any(f in r["features"] for f in features)]
        if not has or any(strict.criterion(f) in strict.default_rejects(r)
                          for r in has for f in features):
            continue
        # a sample that does not depend on the order of the scans: by sha256, as a random key,
        # listed by name
        picks, seen = [], set()
        for r in sorted(has, key=lambda r: r["sha256"]):
            name = (r["package"], r["version"])
            if name not in seen and len(picks) < EXAMPLES:
                seen.add(name)
                picks.append(r)
        picks.sort(key=lambda r: (r["package"].lower(), r["version"] or ""))
        rows = [seen_row(r, short, next((e[0] for f, e in (r.get("examples") or {}).items()
                                         if f in features and e), None)) for r in picks]
        ident, name = matrix.label(case, info).split(" ", 1)
        examples.append(f'<h3 id="{ident}"><a href="{ident}.html"><code>{ident}</code></a> '
                        f"{html.escape(name)}: {len(picks)} of {len(has):,}</h3>\n" + table("seen", rows))
    body = f"""<h1>Seen in source tarballs</h1>
<p>Unlike the test archives, which are crafted, these are real release tarballs: of the
{len(union):,} distinct ones of {ecosystems(names)}, those that cases are seen
in. Each links to where it was downloaded from, with the sha256 that its package pins, and an
example from it where the scan recorded one.</p>
<h2 id="rejected">Rejected by the default policy</h2>
<p>All {len(rejected)} tarballs that the default policy rejects, by why. A tarball with more than
one reason is listed under each.</p>
{table("reasons", summary)}
{chr(10).join(sections)}
<h2 id="accepted">Accepted, with the feature of a case</h2>
<p>For the cases whose tarballs the default policy accepts: a sample of up to {EXAMPLES} of them,
of how many there are, listed by name. The sample is those with the lowest sha256, which is as good
as random, and the same on every run.</p>
{chr(10).join(examples)}
"""
    return page(f"Seen in source tarballs · {TITLE}",
                f"The {len(rejected)} source tarballs that the default policy rejects, and examples "
                "of those that cases are seen in.", body)


def index_page(cases, results, data):
    names, short, rated, union = data
    groups = {}
    for case, info in cases.items():
        groups.setdefault(matrix.category(info), []).append((case, info))
    sections, footnote = [], False
    for group, members in groups.items():
        rows = []
        for case, info in members:
            ident, name = matrix.label(case, info).split(" ", 1)
            features = features_of(case, info)
            k = sum(1 for r in union if any(f in r["features"] for f in features))
            share = prevalence(k, len(union)) if features else "not measured"
            if features and unmeasured(features, union):
                share += '<a href="#unmeasured">*</a>'
                footnote = True
            rows.append(f'<tr><td><a href="{ident}.html"><code>{ident}</code></a></td>'
                        f"<td>{html.escape(name)}</td><td>{inline(info['description'])}</td>"
                        f"<td class=n>{share}</td></tr>")
        sections.append(f"<h3>{html.escape(matrix.GROUPS[group].capitalize())}</h3>\n"
                        + table("cases", rows))
    body = f"""<h1>{TITLE}</h1>
{readme_intro()}
<p>Each case has a permanent identifier, such as F15, whose letter is its category:</p>
<ul>
<li><strong>F</strong> framing: which members an archive has.</li>
<li><strong>N</strong> names: what path each member has.</li>
<li><strong>K</strong> kinds: the mode of each member: file, directory, link or executable.</li>
<li><strong>S</strong> order and state: how members combine into a directory tree.</li>
</ul>
<p>A case's page shows its archive block by block, what every implementation makes of it, and how
common it is in source tarballs.</p>
<h2>Comparison of different tar implementations</h2>
<p>Click a case for its page.</p>
<div class="wide">{matrix.svg(results, cases, lambda case: cases[case]["id"] + ".html")}</div>
<h2 id="policy">Policy</h2>
<p>This section defines the <em>default policy</em><sup><a href="#stricter">1</a></sup>, which
accepts, tolerates or rejects each case below, based on <a href="#tarballs">data</a> from the
{len(union):,} distinct release tarballs of {ecosystems(names)}.</p>
<p>The <em>prevalence</em> column is an estimate of the likelihood of encountering a case in
practice, from a scan of these tarballs.</p>
<p class="note" id="stricter"><sup>1</sup> A policy can be stricter and also reject the tolerated
cases, at the cost of rejecting tarballs that are fairly common. That suits special-purpose tools,
such as an extractor for a single ecosystem, where it can be checked against every tarball ever
published there.</p>
{chr(10).join(sections)}
{UNMEASURED if footnote else ""}
{tarballs_section(names, short, rated, union)}
<h2 id="examples">Motivating examples</h2>
{readme_examples()}
<h2 id="contributing">Contributing</h2>
{readme_section("Contributing")}
"""
    intro = re.sub(r"<[^>]+>", "", readme_intro().split("</p>", 1)[0])
    return page(f"{TITLE} · tar-minefield", html.unescape(intro), body)


def main():
    out, args = sys.argv[1], sys.argv[2:]
    rows, datasets = load(args)
    rated = {n: [r for r in rs if strict.assessed(r)] for n, rs in datasets.items()}
    # ecosystems in every table from the most tarballs to the fewest
    names = sorted(datasets, key=lambda n: (-len(rated[n]), n))
    short = strict.labels(names)
    union = [r for r in rows if strict.assessed(r)]
    data = (names, short, rated, union)
    with open(os.path.join(matrix.HERE, "matrix.json")) as f:
        results = json.load(f)
    cases = matrix.load_cases()
    problems = seen_in_problems(cases, union)
    if problems:
        sys.exit("\n".join(problems))
    os.makedirs(out, exist_ok=True)
    old_pages = {}  # the pages as they are, for the dates they last changed
    for name in os.listdir(out):
        if name.endswith(".html"):
            with open(os.path.join(out, name)) as f:
                old_pages[name] = f.read()
            os.remove(os.path.join(out, name))
    files = {".nojekyll": "", "style.css": STYLE, "index.html": index_page(cases, results, data),
             "seen-in.html": seen_page(cases, data),
             "rejected.html": page(f"Seen in source tarballs · {TITLE}", "Now seen-in.html.",
                                   '<meta http-equiv="refresh" content="0; url=seen-in.html#rejected">\n'
                                   '<p>Now <a href="seen-in.html#rejected">seen-in.html</a>.</p>')}
    for case, info in cases.items():
        files[info["id"] + ".html"] = case_page(case, info, results, data)
    # the pages in order, each with links to the one before and after it, by name, and to the index:
    # in columns that do not change, so that clicking through them the links stay where they are
    sequence = ([("index.html", "all cases")]
                + [(info["id"] + ".html", matrix.label(case, info)) for case, info in cases.items()]
                + [("seen-in.html", "Seen in source tarballs")])
    for i, (name, _) in enumerate(sequence):
        cells = []
        for rel, j in (("prev", i - 1), ("next", i + 1)):
            if 0 <= j < len(sequence):
                label = html.escape(sequence[j][1])
                text = f"‹ {label}" if rel == "prev" else f"{label} ›"
                cells.append(f'<a class="{rel}" href="{sequence[j][0]}" rel="{rel}" title="{label}">'
                             f"{text}</a>")
            else:
                cells.append(f'<span class="{rel}"></span>')
        nav = f'<nav>{cells[0]}<a href="index.html">all cases</a>{cells[1]}</nav>'
        files[name] = files[name].replace("<body>\n", f"<body>\n{nav}\n", 1)
    # every page names its address on the site, so that a copy elsewhere is known as one
    for name in files:
        if name.endswith(".html"):
            address = matrix.SITE + ("" if name == "index.html" else name)
            link = f'<link rel="canonical" href="{address}">\n'
            files[name] = files[name].replace("</head>", link + "</head>", 1)
    for old, new in MOVED.items():
        files[old + ".html"] = page(f"{old} is {new} · tar-minefield", f"{old} is now {new}.",
                                    f'<meta http-equiv="refresh" content="0; url={new}.html">\n'
                                    f'<p>{old} is now <a href="{new}.html">{new}</a>.</p>')
    anchors = set(re.findall(r'id="([^"]+)"', files["seen-in.html"]))
    for name, text in files.items():
        for a in re.findall(r'href="seen-in\.html#([^"]+)"', text):
            if a not in anchors:
                sys.exit(f"{name}: seen-in.html#{a} is not an anchor")
    for name, text in files.items():
        if name.endswith(".html"):
            text = dated(text, old_pages.get(name))
        with open(os.path.join(out, name), "w") as f:
            f.write(text)


if __name__ == "__main__":
    main()

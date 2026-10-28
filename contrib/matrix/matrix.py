"""Run every case of the test suite with every implementation, and tabulate what they make of it.

    python -I contrib/matrix/matrix.py WORK [--only NAME...] [--cases ID...]
    python -I contrib/matrix/matrix.py --readme README.md

Programs are found on PATH, or in an environment variable of their name in capitals, such as
$JULIA or $BSDTAR. WORK is a directory for builds and extractions: runners are built there, and every case is
extracted there in a directory of its own, two levels below a directory that catches what is
written outside it, and N12, whose absolute name is in /tmp, is caught there. Some cases do write
outside the destination in lenient extractors, so WORK should be a throwaway directory. Writes matrix.json, the results, and MATRIX.md, the table made
from them, next to this script. With --only, only the implementations of those names are run, and
their results replace or join those in matrix.json, whose other columns are kept. With --cases,
only the cases of those identifiers, such as F37, are run, and the other rows are kept. With --readme, the summary between `<!-- begin matrix.py -->` and
`<!-- end matrix.py -->` in that file, and MATRIX.md, are generated again from matrix.json, and
nothing is run.

Each implementation extracts every case, and the outcome is compared with the case's verdict:

- ✅ follows the default policy: rejects a case to reject; extracts the expected tree of a case
  to accept
- ➕ accepts a tolerated case, and extracts its expected tree
- ➖ rejects a tolerated case
- ⚠️ accepts a case to reject: the letter says which tree, so that implementations that make
  different trees of one case have different letters. Without a letter, it crashes on the case,
  which is not a rejection: it is killed by a signal, or stopped by a fault in its own code, which
  the runtime of its language raises, as CRASHES says
- ❌ rejects a case to accept, or extracts another tree than the expected one, or crashes on it
- ⏳ does not finish within 60 seconds
- 💥 writes outside the destination
- ❔ not run: matrix.json has no result of the implementation for the case, as when it was not
  installed where the case was first run
"""

import hashlib
import json
import os
import re
import shutil
import signal
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, "suite"))
from check import ABSOLUTE, expected_tree, same  # noqa: E402
import check  # noqa: E402
ARCHIVES = os.path.join(ROOT, "suite", "archives")
RUNNERS = os.path.join(HERE, "runners")
TIMEOUT = 60
# The site, docs/ as contrib/site.py writes it, served as files: a page per case, named by its identifier
SITE = "https://stoppels.ch/tar/"


def run(cmd, **kw):
    """(status, stdout, stderr) of cmd, with status None if it does not finish within TIMEOUT."""
    try:
        p = subprocess.run(cmd, capture_output=True, timeout=TIMEOUT, **kw)
        return p.returncode, p.stdout.decode(errors="replace"), p.stderr.decode(errors="replace")
    except subprocess.TimeoutExpired:
        return None, "", "timeout"


def first_line(cmd):
    code, out, err = run(cmd)
    return (out or err).strip().splitlines()[0] if (out or err).strip() else "?"


TARFILE = (
    "import sys, tarfile\n"
    "try:\n"
    "    with tarfile.open(sys.argv[1]) as t:\n"
    "        t.extractall(sys.argv[2], filter=sys.argv[3])\n"
    "except Exception as e:\n"
    "    sys.exit(f'{type(e).__name__}: {e}')\n"
)


def tool(name):
    """A program from the environment variable of its name in capitals, or from PATH."""
    return os.environ.get(name.upper()) or shutil.which(name)


def fetch_jars(listing, into):
    """The jars that listing names, from Maven Central into a directory, checked by their sha1."""
    import urllib.request

    os.makedirs(into, exist_ok=True)
    for line in open(listing):
        if line.strip() and not line.startswith("#"):
            path, sha1 = line.split()
            target = os.path.join(into, os.path.basename(path))
            if not os.path.exists(target):
                with urllib.request.urlopen(f"https://repo1.maven.org/maven2/{path}") as r:
                    data = r.read()
                if hashlib.sha1(data).hexdigest() != sha1:
                    raise ValueError(f"{path}: sha1 mismatch")
                with open(target, "wb") as f:
                    f.write(data)


def build_mescc_untar(build):
    """The untar of mescc-tools-extra, compiled from the commits of its source.txt, or None."""
    binary = os.path.join(build, "untar")
    if os.path.exists(binary):
        return binary
    sources = {}
    for line in open(os.path.join(RUNNERS, "mescc-tools-extra", "source.txt")):
        if line.strip() and not line.startswith("#"):
            name, url, commit = line.split()
            sources[name] = (url, commit)
    src = os.path.join(build, "src")
    for name, (url, commit) in sources.items():
        path = src if name == "mescc-tools-extra" else os.path.join(src, name)
        shutil.rmtree(path, ignore_errors=True)
        for cmd in (["git", "clone", "-q", "--filter=blob:none", "--no-checkout", url, path],
                    ["git", "-C", path, "checkout", "-q", commit]):
            code, _, err = run(cmd)
            if code != 0:
                print("mescc-tools-extra:", err, file=sys.stderr)
                return None
    # C99: M2libc names a variable bool, which C23 makes a keyword
    code, _, err = run([tool("cc"), "-std=gnu99", "-Wno-implicit-function-declaration", "untar.c",
                        "M2libc/bootstrappable.c", "-o", binary], cwd=src)
    if code != 0:
        print("mescc-tools-extra:", err, file=sys.stderr)
        return None
    return binary


def implementations(work, only=None):
    """(name, version, command) for every implementation found, or of those named in only, with
    command a function of the archive and the destination. Runners of implementations that are
    not wanted are not built."""

    def want(*names):
        return only is None or any(n in only for n in names)

    found = []
    if shutil.which("tar"):
        found.append(("GNU tar", first_line(["tar", "--version"]),
                      lambda a, d: ["tar", "-xf", a, "-C", d]))
    bsdtar = tool("bsdtar")
    if bsdtar:
        found.append(("bsdtar", first_line([bsdtar, "--version"]).split(" zlib")[0],
                      lambda a, d, b=bsdtar: [b, "-xf", a, "-C", d]))
    if want("live-bootstrap untar", "live-bootstrap untar, --non-strict") and shutil.which("git") \
            and tool("cc"):
        binary = build_mescc_untar(os.path.join(work, "build", "mescc-tools-extra"))
        if binary:
            commit = open(os.path.join(RUNNERS, "mescc-tools-extra", "source.txt")).read().split(
                "mescc-tools-extra https://github.com/oriansj/mescc-tools-extra ")[1][:12]
            version = f"mescc-tools-extra {commit}, as live-bootstrap pins it, built with cc"
            # untar exits 0 when it "produced errors", such as a checksum failure: as an error
            check = ('out=$("$@" 2>&1); code=$?; printf "%s\\n" "$out" >&2; '
                     'case $out in *"produced errors"*) exit 1;; esac; exit $code')
            found.append(("live-bootstrap untar", version,
                          lambda a, d, b=binary: ["sh", "-c", check, "sh", b, "--file", a]))
            found.append(("live-bootstrap untar, --non-strict", version,
                          lambda a, d, b=binary: ["sh", "-c", check, "sh", b, "--non-strict",
                                                  "--file", a]))
    busybox = tool("busybox")
    if busybox:
        # without the time of the build, which a build from source has in its banner
        version = re.sub(r" \(\d{4}-\d\d-\d\d [^)]*\)", "",
                         first_line([busybox]).split(" multi-call")[0])
        found.append(("BusyBox tar", version + ", defconfig",
                      lambda a, d: [busybox, "tar", "-xf", a, "-C", d]))
    sevenzip = tool("7z")
    if sevenzip:
        code, out, _ = run([sevenzip])
        version = next((l for l in out.splitlines() if l.startswith("7-Zip")), "7-Zip").split(" :")[0]
        found.append(("7-Zip", version,
                      lambda a, d: [sevenzip, "x", "-y", "-bd", f"-o{d}", a]))
    python = sys.executable
    pyversion = f"CPython {sys.version.split()[0]}"
    # pip's untar_file is the data filter, after it strips a leading directory that all members share
    for f, name in (("fully_trusted", "fully_trusted"), ("tar", "tar"), ("data", "data, as in pip")):
        found.append((f"Python tarfile, filter={name}", pyversion,
                      lambda a, d, f=f: [python, "-I", "-c", TARFILE, a, d, f]))
    build = os.path.join(work, "build")
    os.makedirs(build, exist_ok=True)
    if want("Go containerd archive.Apply") and shutil.which("go"):
        binary = os.path.join(build, "containerd-runner")
        code, _, err = run(["go", "build", "-o", binary, "."], cwd=os.path.join(RUNNERS, "containerd"))
        if code == 0:
            found.append(("Go containerd archive.Apply", first_line([binary, "--version"]),
                          lambda a, d, b=binary: [b, a, d]))
        else:
            print("containerd runner:", err, file=sys.stderr)
    if want("Rust tar", "Rust astral-tokio-tar", "Rust tar-codec, as in uv") and shutil.which("cargo"):
        target = os.path.join(build, "rust")
        code, _, err = run(["cargo", "build", "--release", "--quiet", "--target-dir", target],
                           cwd=os.path.join(RUNNERS, "rust"))
        if code == 0:
            binary = os.path.join(target, "release", "runner")
            found.append(("Rust tar", "tar 0.4.46, unpack",
                          lambda a, d, b=binary: [b, "tar", a, d]))
            found.append(("Rust astral-tokio-tar", "astral-tokio-tar 0.7.0, unpack",
                          lambda a, d, b=binary: [b, "astral-tokio-tar", a, d]))
            found.append(("Rust tar-codec, as in uv", "tar-codec 0.0.15, with the policies of uv 0.13",
                          lambda a, d, b=binary: [b, "tar-codec-uv", a, d]))
        else:
            print("rust runner:", err, file=sys.stderr)
    cabal = tool("cabal")
    if want("Haskell tar") and cabal:
        target = os.path.join(build, "haskell")
        code, out, err = run([cabal, "install", "--installdir", target, "--overwrite-policy=always",
                              "--install-method=copy", f"--builddir={target}/dist"],
                             cwd=os.path.join(RUNNERS, "haskell"))
        if code == 0:
            version = first_line([os.path.join(target, "runner"), "--version"])
            found.append(("Haskell tar", version,
                          lambda a, d, b=os.path.join(target, "runner"): [b, a, d]))
        else:
            print("haskell runner:", (err or out)[-2000:], file=sys.stderr)
    java = tool("java")
    if want("Java Commons Compress") and java:
        jars = os.path.join(build, "java")
        fetch_jars(os.path.join(RUNNERS, "java", "jars.txt"), jars)
        java_version = first_line([java, "-version"]).split('"')[1]
        found.append(("Java Commons Compress", f"Commons Compress 1.28.0, Expander, on Java {java_version}",
                      lambda a, d, j=java, c=os.path.join(jars, "*"):
                      [j, "-cp", c, os.path.join(RUNNERS, "java", "Extract.java"), a, d]))
    dotnet = tool("dotnet")
    if want(".NET System.Formats.Tar") and dotnet:
        # built in a copy, as dotnet writes obj/ next to the project
        src = os.path.join(build, "dotnet")
        shutil.copytree(os.path.join(RUNNERS, "dotnet"), src, dirs_exist_ok=True)
        code, out, err = run([dotnet, "build", "-c", "Release", "-o", os.path.join(src, "out"),
                              "--nologo", "-v", "q"], cwd=src)
        if code == 0:
            binary = os.path.join(src, "out", "runner")
            found.append((".NET System.Formats.Tar", first_line([binary, "--version"]),
                          lambda a, d, b=binary: [b, a, d]))
        else:
            print("dotnet runner:", (out or err)[-2000:], file=sys.stderr)
    ruby = tool("ruby")
    if ruby:
        code, out, _ = run([ruby, "-e", 'require "rubygems"; print Gem::VERSION, " ", RUBY_VERSION'])
        version = "RubyGems {} of Ruby {}, extract_tar_gz".format(*out.split()) if code == 0 else "?"
        found.append(("RubyGems", version, lambda a, d, r=ruby:
                      [r, os.path.join(RUNNERS, "ruby", "extract.rb"), a, d]))
    php = tool("php")
    if want("PHP PharData, as in Composer") and php:
        script = os.path.join(RUNNERS, "php", "extract.php")
        php_version = first_line([php, "-r", "echo PHP_VERSION;"])
        found.append(("PHP PharData, as in Composer", f"PharData of PHP {php_version}, as Composer's"
                      " TarDownloader calls it", lambda a, d, p=php, s=script:
                      [p, "-d", "display_errors=stderr", s, a, d]))
    rscript = tool("Rscript")
    if want("R untar, internal") and rscript:
        script = os.path.join(RUNNERS, "r", "extract.R")
        version = first_line([rscript, "-e", 'cat(format(getRversion()))'])
        found.append(("R untar, internal", f'utils::untar of R {version}, tar = "internal"',
                      lambda a, d, r=rscript, s=script: [r, "--vanilla", s, a, d]))
    perl = tool("perl")
    if perl:
        code, out, _ = run([perl, "-MArchive::Tar", "-e", 'print "$Archive::Tar::VERSION $^V"'])
        version = "Archive::Tar {} of Perl {}".format(*out.split()) if code == 0 else "?"
        found.append(("Perl Archive::Tar", version, lambda a, d, p=perl:
                      [p, os.path.join(RUNNERS, "perl", "extract.pl"), a, d]))
    julia = tool("julia")
    if julia:
        script = os.path.join(RUNNERS, "julia", "extract.jl")
        code, out, _ = run([julia, "--startup-file=no", "-e",
                            'using Tar; print(VERSION, " ", pkgversion(Tar))'])
        version = "Tar {1} of Julia {0}".format(*out.split()) if code == 0 else "?"
        found.append(("Julia Tar.jl", version,
                      lambda a, d, j=julia, s=script: [j, "--startup-file=no", s, a, d]))
    if want("node-tar", "node-tar, strict", "tar-fs") and shutil.which("npm"):
        node = os.path.join(build, "node")
        shutil.copytree(os.path.join(RUNNERS, "node"), node, dirs_exist_ok=True)
        code, _, err = run(["npm", "ci", "--silent", "--no-audit", "--no-fund"], cwd=node)
        if code == 0:
            script = os.path.join(node, "extract.js")
            found.append(("node-tar", "tar 7.5.22",
                          lambda a, d, s=script: ["node", s, a, d]))
            found.append(("node-tar, strict", "tar 7.5.22",
                          lambda a, d, s=script: ["node", s, a, d, "strict"]))
            found.append(("tar-fs", "tar-fs 3.1.3, on tar-stream 3.2.2",
                          lambda a, d, s=os.path.join(node, "tar-fs.js"): ["node", s, a, d]))
        else:
            print("node runner:", err, file=sys.stderr)
    return [i for i in found if want(i[0])]


def extract(command, archive, root):
    """Extract into root/x/y/dest; return (status, error, tree, outside), where outside is what
    was written in root but not under dest."""
    dest = os.path.join(root, "x", "y", "dest")
    code, out, err, tree, outside = check.extract(command, archive, root, TIMEOUT)
    error = None
    if code != 0:
        error = (err.strip() or out.strip()
                 or (f"killed by {signal.Signals(-code).name}" if code < 0 else f"status {code}"))
        error = error.replace(dest, "DEST").replace(root, "ROOT")
        # Node shortens a long path in its messages to a prefix and "...", which depends on
        # where WORK is
        work = os.path.dirname(os.path.dirname(os.path.dirname(root)))
        for k in range(len(dest), len(work), -1):
            error = error.replace(dest[:k] + "...", "DEST...")
        error = error.replace(ROOT + os.sep, "")
        if len(error) > 300:
            # the message comes first, and what follows is where it was raised
            error = error[:300].rsplit(None, 1)[0] + " …"
    return code, error, tree, outside


def text(name):
    """A name as it can be shown in code: other bytes than UTF-8, control characters and backticks,
    which would end the code, escaped."""
    name = name.encode("utf-8", "surrogateescape").decode("utf-8", "backslashreplace")
    return "".join(c if c.isprintable() and c != "`" else f"\\x{ord(c):02x}" for c in name)


def describe(tree):
    """A tree as a short text, to tell trees apart in the table."""
    parts = []
    for path in sorted(tree):
        e = tree[path]
        path = text(path)
        if e["kind"] == "directory":
            parts.append(f"`{path}/`")
        elif e["kind"] == "symlink":
            parts.append(f"`{path}` → `{text(e['target'])}`")
        elif e["kind"] == "file":
            parts.append(f"`{path}` ({e['size']} B, {e['sha256'][:8]})")
        else:
            parts.append(f"`{path}` ({e['kind']})")
    return ", ".join(parts) or "nothing"


GROUPS = {
    "accept": "to accept",
    "tolerate": "tolerated",
    "framing": "to reject: framing",
    "name": "to reject: names",
    "kind": "to reject: kinds",
    "order and state": "to reject: order and state",
}


def category(info):
    """The group of a case: its verdict, and for cases to reject the category that
    scanner/strict.py gives its features; a case without any is one the scanner cannot read
    past, which is framing."""
    if info["verdict"] != "reject":
        return info["verdict"]
    sys.path.insert(0, os.path.join(HERE, "..", "scanner"))
    import strict

    categories = [strict.classify(f)[1] for f in info["features"]
                  if strict.classify(f)[0] == "strict"]
    return categories[0] if categories else "framing"


def label(case, info):
    """The identifier of a case and its name: `F15 pax-size-on-dir`, of `F15-pax-size-on-dir`."""
    return case.replace("-", " ", 1)


def load_cases():
    """The cases, in the order of GROUPS, and by identifier in each group."""
    cases = {}
    for name in sorted(os.listdir(ARCHIVES)):
        if name.endswith(".json"):
            with open(os.path.join(ARCHIVES, name)) as f:
                cases[name[:-5]] = json.load(f)
    order = list(GROUPS)
    return dict(sorted(cases.items(), key=lambda kv: (order.index(category(kv[1])), kv[1]["id"])))


def main():
    if sys.argv[1] == "--readme":
        with open(os.path.join(HERE, "matrix.json")) as f:
            results = json.load(f)
        cases = load_cases()
        readme(sys.argv[2], results, cases)
        write_outputs(results, cases)
        return
    work = os.path.abspath(sys.argv[1])
    options, names = {}, None
    for arg in sys.argv[2:]:
        if arg in ("--only", "--cases"):
            names = options.setdefault(arg, set())
        elif names is None:
            sys.exit(f"{arg}: expected --only or --cases")
        else:
            names.add(arg)
    only, ids = options.get("--only"), options.get("--cases")
    if os.path.lexists(ABSOLUTE):
        sys.exit(f"{ABSOLUTE} exists, and would count as written by the first extractor: "
                 "remove it first")
    cases = load_cases()
    unknown = (ids or set()) - {info["id"] for info in cases.values()}
    if unknown:
        sys.exit(f"no such cases: {' '.join(sorted(unknown))}")
    impls = implementations(work, only)
    results = {"implementations": [{"name": n, "version": v} for n, v, _ in impls],
               "cases": {}}
    if only or ids:
        # the other columns, and those of names in only that were not found, are kept as they are
        # in matrix.json, and so are the other rows
        with open(os.path.join(HERE, "matrix.json")) as f:
            previous = json.load(f)
        ran = {name for name, _, _ in impls}
        results["implementations"] = [i for i in previous["implementations"]
                                      if i["name"] not in ran] + results["implementations"]
    runs = os.path.join(work, "runs")
    shutil.rmtree(runs, ignore_errors=True)
    for case, info in cases.items():
        if ids and info["id"] not in ids:
            results["cases"][case] = previous["cases"][case]
            continue
        archive = os.path.join(ARCHIVES, case + ".tar")
        row = dict(previous["cases"].get(case, {})) if only else {}
        for i, (name, version, command) in enumerate(impls):
            code, error, tree, outside = extract(command, archive, os.path.join(runs, str(i), case))
            row[name] = {"error": error, "tree": tree, "outside": outside}
            if code is None:
                # a run that does not finish has not rejected the case, whatever it wrote so far
                row[name]["timeout"] = True
            elif code < 0:
                # nor has a run that is killed by a signal, such as a segfault
                row[name]["signal"] = -code
        results["cases"][case] = row
        print(case, file=sys.stderr)
    with open(os.path.join(HERE, "matrix.json"), "w") as f:
        json.dump(results, f, indent=1, sort_keys=True)
        f.write("\n")
    write_outputs(results, cases)


# Errors that are a crash rather than a rejection: a fault in the implementation's own code, which
# the runtime of its language raises, such as a null where a string belongs, or an index out of
# bounds. An error that the implementation raises itself is a rejection, and so is one of the system
# or the file API of its platform, which refuses an operation or a path (a link to nothing, a NUL in
# a path), or of a function that parses a number, which refuses one that is not.
CRASHES = re.compile(
    r"TypeError \[ERR_INVALID_ARG_TYPE\]: .* Received null"  # Node, given a null for a string
    r"|TypeError: |IndexError: |AttributeError: |RecursionError: "  # Python
    r"|BoundsError: |MethodError: "  # Julia
    r"|argument must be coercible to non-negative integer|the condition has length > 1"
    r"|embedded nul in string: "  # R, on an NA, -Inf or NUL of its own making
    r"|NoMethodError: "  # Ruby
    r"|\S*(NullPointer|ArrayIndexOutOfBounds|StringIndexOutOfBounds)Exception"  # Java
    r"|(NullReference|IndexOutOfRange)Exception: "  # .NET
    r"|panic: |thread '.*' panicked at "  # Go, Rust
    r"|Prelude\.")  # Haskell, such as Prelude.head of an empty list


def crashed(r):
    """Whether a run crashed: killed by a signal, or stopped by a fault in its own code."""
    return bool(r.get("signal") or r["error"] and CRASHES.match(r["error"]))


def outcome(case, r):
    """(symbol, tree or None) of one run, or of None where there was no run."""
    if r is None:
        return "❔", None
    if r["outside"]:
        return "💥", None
    if r.get("timeout"):
        return "⏳", None
    if crashed(r):
        # a crash, without the letter of a tree: what it wrote before it was killed is not a tree
        # it chose
        return ("⚠️" if case["verdict"] == "reject" else "❌"), None
    if case["verdict"] == "reject":
        return ("✅", None) if r["error"] else ("⚠️", r["tree"])
    tolerated = case["verdict"] == "tolerate"
    if r["error"]:
        return ("➖" if tolerated else "❌"), None
    if r["tree"] is None or same(r["tree"], expected_tree(case)):
        return ("➕" if tolerated else "✅"), None
    return "❌", r["tree"]


ORDER = ["✅", "➕", "➖", "⚠️", "❌", "⏳", "💥", "❔"]
LEGEND = [
    "- ✅ follows the default policy: rejects a case to reject; extracts the expected tree of a"
    " case to accept",
    "- ➕ accepts a tolerated case, and extracts its expected tree; ➖ rejects a tolerated case",
    "- ⚠️ accepts a case to reject. The letter is the tree it extracts: in one row, the same letter is"
    " the same tree, and different letters are trees that differ; [MATRIX.md](MATRIX.md#trees)"
    " lists them. Without a letter, it crashes on the case, which is not a rejection",
    "- ❌ rejects a case to accept, or extracts another tree than the expected one, or crashes on it",
    f"- ⏳ does not finish within {TIMEOUT} seconds",
    "- 💥 writes outside the destination",
    "- ❔ not run: the implementation was not installed where the case was run",
]
# The order of the columns, roughly by how widely used an implementation is: command-line tools,
# then libraries by the popularity of their language, and niche tools last. Others go at the end.
POPULARITY = [
    "GNU tar", "bsdtar", "BusyBox tar", "7-Zip",
    "Python tarfile, filter=data, as in pip", "Python tarfile, filter=tar",
    "Python tarfile, filter=fully_trusted",
    "node-tar", "node-tar, strict", "tar-fs",
    "Java Commons Compress", ".NET System.Formats.Tar",
    "PHP PharData, as in Composer",
    "Go containerd archive.Apply",
    "Rust tar", "Rust astral-tokio-tar", "Rust tar-codec, as in uv",
    "RubyGems", "R untar, internal", "Perl Archive::Tar", "Haskell tar", "Julia Tar.jl",
    "live-bootstrap untar", "live-bootstrap untar, --non-strict",
]
# The page of every implementation on the site, by a name of its own: the column may be renamed,
# as its version or how it is called is said more precisely, and the address of its page stays
SLUGS = {
    "GNU tar": "gnu-tar",
    "bsdtar": "bsdtar",
    "BusyBox tar": "busybox",
    "7-Zip": "7zip",
    "Python tarfile, filter=data, as in pip": "tarfile-data",
    "Python tarfile, filter=tar": "tarfile-tar",
    "Python tarfile, filter=fully_trusted": "tarfile-trusted",
    "node-tar": "node-tar",
    "node-tar, strict": "node-tar-strict",
    "tar-fs": "tar-fs",
    "Java Commons Compress": "commons-compress",
    ".NET System.Formats.Tar": "dotnet",
    "PHP PharData, as in Composer": "phardata",
    "Go containerd archive.Apply": "containerd",
    "Rust tar": "rust-tar",
    "Rust astral-tokio-tar": "astral-tokio-tar",
    "Rust tar-codec, as in uv": "tar-codec",
    "RubyGems": "rubygems",
    "R untar, internal": "r-untar",
    "Perl Archive::Tar": "archive-tar",
    "Haskell tar": "haskell-tar",
    "Julia Tar.jl": "julia-tar",
    "live-bootstrap untar": "live-bootstrap",
    "live-bootstrap untar, --non-strict": "live-bootstrap-nonstrict",
}


def ordered(results):
    """The implementations of the results, in the order of POPULARITY."""
    rank = {n: i for i, n in enumerate(POPULARITY)}
    return sorted(results["implementations"], key=lambda i: rank.get(i["name"], len(rank)))


def count_implementations(names):
    """How many implementations the columns are: a column is an implementation or one of its
    configurations, such as a filter of tarfile, named after a comma."""
    return len({n.split(",")[0] for n in names})


def columns(results):
    return [i["name"] for i in ordered(results)]


def case_cells(info, row, names):
    """The cell of every implementation for one case, and the trees its letters stand for."""
    letters, cells = {}, {}
    for n in names:
        symbol, tree = outcome(info, row.get(n))
        cells[n] = symbol
        if tree is not None:
            key = describe(tree)
            letters.setdefault(key, chr(ord("A") + len(letters)))
            cells[n] = symbol + letters[key]
    return cells, letters


def totals(results, cases, names):
    counts = {n: {} for n in names}
    for case, info in cases.items():
        for n in names:
            symbol = outcome(info, results["cases"].get(case, {}).get(n))[0]
            counts[n][symbol] = counts[n].get(symbol, 0) + 1
    return {n: " ".join(f"{s}{counts[n][s]}" for s in ORDER if counts[n].get(s)) for n in names}


# SVG: the classes of outcomes; their colours as (cell, mark): pale cells, as a grid of saturated
# ones flickers at its crossings; what they mean; and a mark that tells them apart without colour.
# The SVG has a white background of its own, so that it looks the same in light and dark mode.
# The two outcomes of a tolerated case are greys, as neither is better than the other; that of
# accepting is the paler, as most implementations do, so that the few that reject stand out.
CLASSES = {
    "✅": ("ok", ("#b4f1c3", "#116329"),
          "follows the default policy: rejects a case to reject, extracts the expected tree of a "
          "case to accept", "✓"),
    "➕": ("may-accept", ("#e6eaef", "#424a53"),
          "accepts a tolerated case and extracts its expected tree", "+"),
    "➖": ("may-reject", ("#c4ccd4", "#24292f"),
          "rejects a tolerated case", "−"),
    "⚠️": ("warn", ("#ffe08a", "#7d4e00"),
           "accepts a case to reject, or crashes on it", "!"),
    "❌": ("bad", ("#ffc1ba", "#a40e26"),
           "rejects a case to accept, or extracts another tree than the expected one, or crashes on it",
           "✗"),
    "⏳": ("slow", ("#b6e3ff", "#0550ae"),
           f"does not finish within {TIMEOUT} seconds", "…"),
    "💥": ("boom", ("#dcc8ff", "#6639ba"),
           "writes outside the destination", "↑"),
    "❔": ("none", ("#ffffff", "#59636e"),
          "not run: the implementation was not installed where the case was run", "?"),
}
FONT = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"


def group(name):
    """The group of an implementation, which the SVG separates from the next by a gap: the
    command-line tools, the libraries of each language, and live-bootstrap."""
    if name in ("GNU tar", "bsdtar", "BusyBox tar", "7-Zip"):
        return "tool"
    if name == "tar-fs":
        return "node-tar"
    return name.split()[0].replace("RubyGems", "Ruby").replace("node-tar,", "node-tar")


def esc(text):
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def svg_style():
    colours = "".join(f".{cls}{{fill:{fill}}}.{cls}-ink{{fill:{ink}}}"
                      for cls, (fill, ink) in {c[0]: c[1] for c in CLASSES.values()}.items())
    return (
        f"<style>text{{font-family:{FONT};font-size:12px;fill:#1f2328}}.head{{font-weight:600}}"
        f".cell{{font-size:11px;font-weight:700;text-anchor:middle}}.rule{{stroke:#d0d7de}}{colours}"
        ".id{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace}"
        ".none{stroke:#8c959f;stroke-dasharray:2 2}.hit{fill:transparent}a.row:hover .hit{fill:#eaeef2}a.row:hover .name{text-decoration:underline}"
        '</style><rect width="100%" height="100%" fill="#ffffff"/>'
    )


def cell_svg(x, y, w, h, symbol):
    """A cell, coloured and marked by its outcome. Which tree an implementation extracts is left
    to MATRIX.md and the page of the case, which list the trees."""
    base = next(c for c in CLASSES if symbol.startswith(c))
    cls, mark = CLASSES[base][0], CLASSES[base][3]
    return (f'<rect class="{cls}" x="{x}" y="{y}" width="{w}" height="{h}" rx="3"/>'
            f'<text class="cell {cls}-ink" x="{x + w / 2}" y="{y + h / 2 + 4}">{mark}</text>')


def used(results, cases):
    """The outcomes that some cell has, so that a legend leaves out the others."""
    names = columns(results)
    return {outcome(info, results["cases"].get(case, {}).get(n))[0]
            for case, info in cases.items() for n in names}


def legend_svg(x, y, symbols):
    out = []
    for c in (CLASSES[s] for s in CLASSES if s in symbols):
        out.append(f'<rect class="{c[0]}" x="{x}" y="{y - 12}" width="16" height="16" rx="3"/>'
                   f'<text class="cell {c[0]}-ink" x="{x + 8}" y="{y}">{c[3]}</text>'
                   f'<text x="{x + 22}" y="{y}">{esc(c[2])}</text>')
        y += 21
    return "".join(out), y


def svg(results, cases, link=None, column_link=None):
    """Every implementation in columns; in rows, the outcomes of all cases first, as a bar per
    implementation, then every case, labelled by its identifier on the left and its name on the
    right, so that on a narrow screen the cells come right after the identifiers; with link(case)
    a link to its page, and with column_link(name) one to the page of an implementation, on its
    name. Links work where the SVG is part of the page, not where it is an image."""
    names = columns(results)
    counts = {n: {} for n in names}
    for case, info in cases.items():
        for n in names:
            symbol = outcome(info, results["cases"].get(case, {}).get(n))[0]
            counts[n][symbol] = counts[n].get(symbol, 0) + 1
    left = 20 + 7 * max(len(i["id"]) for i in cases.values())
    cw, ch, gap, top = 22, 16, 2, 230
    xs, x, previous = {}, left, None
    for n in names:
        if previous is not None and group(n) != group(previous):
            x += 10
        xs[n], previous, x = x, n, x + cw + gap
    right = x - gap + 10
    end = right + 7 * max(len(label(c, i).split(" ", 1)[1]) for c, i in cases.items())
    out, y = [], top
    for n in names:
        name = f'<text transform="translate({xs[n] + cw / 2 + 4},{top - 8}) rotate(-60)">{esc(n)}</text>'
        out.append(f'<a class="column" href="{esc(column_link(n))}">{name}</a>' if column_link else name)
    if column_link:
        # only with the links, so that the SVG without them, and the images made of it, stay the same
        out.append("<style>a.column:hover text{fill:#0969da;text-decoration:underline}</style>")
    # the bars: outcomes stacked from the bottom, with the number of each where it fits
    bar = 2 * len(cases)
    out.append(f'<text x="{right}" y="{y + bar / 2 + 4}">all {len(cases)} cases</text>')
    for n in names:
        bottom = y + bar
        for symbol in ORDER:
            k = counts[n].get(symbol, 0)
            if not k:
                continue
            h = bar * k / len(cases)
            out.append(f'<g><title>{esc(n)}: {k} of {len(cases)}, {esc(CLASSES[symbol][2])}</title>'
                       f'<rect class="{CLASSES[symbol][0]}" x="{xs[n]}" y="{bottom - h:.1f}" '
                       f'width="{cw}" height="{h:.1f}"/>')
            if h >= 14:
                out.append(f'<text class="cell {CLASSES[symbol][0]}-ink" x="{xs[n] + cw / 2}" '
                           f'y="{bottom - h / 2 + 4:.1f}">{k}</text>')
            # a white line between outcomes, which tells apart the two of one colour
            out.append(f'<line x1="{xs[n]}" x2="{xs[n] + cw}" y1="{bottom - h:.1f}" '
                       f'y2="{bottom - h:.1f}" stroke="#ffffff"/></g>')
            bottom -= h
    y += bar
    previous = None
    for case, info in cases.items():
        if category(info) != previous:
            previous = category(info)
            out.append(f'<line class="rule" x1="10" x2="{end}" y1="{y + 10}" y2="{y + 10}"/>'
                       f'<text class="head" x="10" y="{y + 26}">{esc(GROUPS[previous])}</text>')
            y += 34
        # with links, the whole row is one, over a rect that highlights it on hover
        if link:
            out.append(f'<a class="row" href="{esc(link(case))}"><rect class="hit" x="10" '
                       f'y="{y - gap / 2}" width="{end - 10}" height="{ch + gap}" rx="3"/>')
        ident, name = label(case, info).split(" ", 1)
        out.append(f'<text class="name id" x="{left - 10}" y="{y + ch / 2 + 4}" text-anchor="end">'
                   f'{esc(ident)}</text><text class="name" x="{right}" y="{y + ch / 2 + 4}">'
                   f"{esc(name)}</text>")
        cells, _ = case_cells(info, results["cases"].get(case, {}), names)
        for n in names:
            out.append(cell_svg(xs[n], y, cw, ch, cells[n]))
        if link:
            out.append("</a>")
        y += ch + gap
    legend, y = legend_svg(left, y + 24, used(results, cases))
    out.append(legend)
    # the rotated name of the last column reaches past it, by the cosine of 60°
    width, height = int(max(x + 20 + 7 * len(names[-1]) / 2, end + 10)), y + 4
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
            f'viewBox="0 0 {width} {height}" role="img"><title>What implementations make of every '
            f'case of the test suite</title>{svg_style()}{"".join(out)}</svg>\n')


def write_outputs(results, cases):
    """MATRIX.md and matrix.svg, from the results."""
    for name, data in (("MATRIX.md", table(results, cases)), ("matrix.svg", svg(results, cases))):
        with open(os.path.join(HERE, name), "w") as f:
            f.write(data)


def readme(path, results, cases):
    """The summary in the README: matrix.svg, with the outcomes of every implementation as text."""
    names = columns(results)
    total = totals(results, cases, names)
    lines = [
        f"What {count_implementations(names)} implementations make of the {len(cases)} cases: a "
        "row per case, by category, and a column per implementation, with the outcomes of all "
        "cases at the top. "
        f"[The website]({SITE}) has a page per case.",
        "",
        "[![What every implementation makes of every case of the test suite. Outcomes of all cases: "
        + "; ".join(f"{n}: {total[n]}" for n in names) + f"](contrib/matrix/matrix.svg)]({SITE})",
    ]
    block = "\n".join(lines)
    text = open(path).read()
    begin, end = "<!-- begin matrix.py -->", "<!-- end matrix.py -->"
    head, rest = text.split(begin, 1)
    _, tail = rest.split(end, 1)
    with open(path, "w") as f:
        f.write(f"{head}{begin}\n{block}\n{end}{tail}")


def table(results, cases):
    names = columns(results)
    lines = [
        "# What implementations make of the test suite",
        "",
        "Generated by `matrix.py` from `matrix.json`: every case of [suite/archives/](../../suite/archives),",
        "extracted by every implementation.",
        "",
    ] + [line for line in LEGEND if line.split()[1] in used(results, cases)] + [
        "",
        "![Every case of the test suite, in rows, and what every implementation makes of it, in columns:"
        " the table below as a picture](matrix.svg)",
        "",
        "| implementation | version |",
        "|---|---|",
    ]
    for i in ordered(results):
        lines.append(f"| {i['name']} | {i['version']} |")
    lines.append("")
    header = "| case | " + " | ".join(names) + " |"
    lines += [header, "|---|" + "---|" * len(names)]
    notes = []
    previous = None
    for case, info in cases.items():
        if category(info) != previous:
            previous = category(info)
            lines.append(f"| **{GROUPS[previous]}** |" + " |" * len(names))
        cells, letters = case_cells(info, results["cases"].get(case, {}), names)
        ident, name = label(case, info).split(" ", 1)
        lines.append(f"| [{ident}]({SITE}{ident}.html) {name} | "
                     + " | ".join(cells[n] for n in names) + " |")
        if letters:
            notes.append(f"- {ident} {name}: " + "; ".join(f"{l}: {k}" for k, l in letters.items()))
    total = totals(results, cases, names)
    lines.append("| **total** | " + " | ".join(total[n] for n in names) + " |")
    lines += ["", "## Trees", "", "What the implementations that accept a case extract, where it is"
              " not the expected tree: files by their size and the start of their sha256.", ""]
    lines += notes
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    main()

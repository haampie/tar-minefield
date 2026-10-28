"""Check an extractor against the test suite.

    python -I suite/check.py [--case ID[,ID...]]... -- COMMAND...

COMMAND extracts one archive. In its arguments, `{archive}` is replaced by the archive and `{dest}`
by the empty directory to extract it into, which is also its working directory, and its standard
input is the archive. An exit status other than 0 is a rejection. With --case, only the cases
of those identifiers are run: it can be repeated, and takes a list separated by commas, such as
`--case F37 --case 'N27, N28'`. For example:

    python -I suite/check.py -- tar -xf '{archive}' -C '{dest}'

The placeholders are quoted, since a shell reads `{dest}` before a redirection as a redirection.

Every case is extracted in a temporary directory of its own, as root/x/y/dest, so that what is
written in root but not under dest is caught, and so is the absolute name of N12, in /tmp. A case
passes if the extractor rejects a case to reject, extracts the expected tree of a case to accept,
and either rejects a tolerated case or extracts its tree; and in every case if it writes nothing
outside dest, is not killed by a signal, and finishes within TIMEOUT seconds. Each case is printed
with what the extractor did, and the exit status is 1 if a case fails.

Tests of a library in Python can import this module: extract into a directory, and call
problems(case, status, walk(dest)), with status 0 if the library extracted the archive and 1 if it
rejected it, which is empty if the case passes.

It needs nothing outside suite/ but the Python standard library.
"""

import hashlib
import json
import os
import shutil
import signal
import stat
import subprocess
import sys
import tempfile
import textwrap

HERE = os.path.dirname(os.path.abspath(__file__))
ARCHIVES = os.path.join(HERE, "archives")
TIMEOUT = 60
# The absolute name of N12: in /tmp, which an extractor that follows it can write without root
ABSOLUTE = "/tmp/tar-minefield-absolute"


def run(cmd, timeout=TIMEOUT, **kw):
    """(status, stdout, stderr) of cmd, with status None if it does not finish within timeout."""
    try:
        p = subprocess.run(cmd, capture_output=True, timeout=timeout, **kw)
        return p.returncode, p.stdout.decode(errors="replace"), p.stderr.decode(errors="replace")
    except subprocess.TimeoutExpired:
        return None, "", "timeout"


def entry(path, dest=None):
    """The entry of one path, as in the expected trees of the cases. Link targets in dest start with
    `DEST` instead, so that the results do not depend on where they were made."""
    st = os.lstat(path)
    if stat.S_ISLNK(st.st_mode):
        target = os.readlink(path)
        if dest and (target == dest or target.startswith(dest + os.sep)):
            target = "DEST" + target[len(dest):]
        return {"kind": "symlink", "target": target}
    if stat.S_ISDIR(st.st_mode):
        return {"kind": "directory"}
    if stat.S_ISREG(st.st_mode):
        with open(path, "rb") as f:
            data = f.read()
        return {"kind": "file", "size": len(data), "sha256": hashlib.sha256(data).hexdigest(),
                "executable": bool(st.st_mode & stat.S_IXUSR)}
    return {"kind": "other"}


def walk(top, dest=None):
    """The tree under top: {path: entry}, without following links to directories."""
    tree = {}
    for dirpath, dirnames, filenames in os.walk(top):
        for name in dirnames + filenames:
            path = os.path.join(dirpath, name)
            tree[os.path.relpath(path, top).replace(os.sep, "/")] = entry(path, dest)
        dirnames[:] = [d for d in dirnames if not os.path.islink(os.path.join(dirpath, d))]
    return tree


def expected_tree(case):
    return {e["path"]: {k: v for k, v in e.items() if k != "path"} for e in case["tree"]}


def same(tree, expected):
    """Whether a tree is the expected one, comparing what that says of each entry."""
    if set(tree) != set(expected):
        return False
    for path, e in expected.items():
        got = tree[path]
        if any(got.get(k) != v for k, v in e.items()):
            return False
    return True


def extract(command, archive, root):
    """Run command(archive, dest), which extracts archive into dest, root/x/y/dest, with the
    archive as its standard input. Return (status, stdout, stderr, tree, outside), where status is
    None if it does not finish within TIMEOUT, dest is DEST and root is ROOT in stdout and stderr,
    and outside is what was written in root but not under dest, or at ABSOLUTE, which is removed."""
    dest = os.path.join(root, "x", "y", "dest")
    os.makedirs(dest)
    with open(archive, "rb") as stdin:
        status, out, err = run(command(archive, dest), cwd=dest, stdin=stdin)
    out, err = (s.replace(dest, "DEST").replace(root, "ROOT") for s in (out, err))
    tree = walk(dest, dest)
    outside = {p: e for p, e in walk(root, dest).items()
               if p not in ("x", "x/y", "x/y/dest") and not p.startswith("x/y/dest/")}
    if os.path.lexists(ABSOLUTE):
        outside[ABSOLUTE] = entry(ABSOLUTE)
        if os.path.isdir(ABSOLUTE) and not os.path.islink(ABSOLUTE):
            shutil.rmtree(ABSOLUTE)
        else:
            os.remove(ABSOLUTE)
    return status, out, err, tree, outside


def classify(case, status, tree, outside, crashed=False):
    """What a run did with a case: "outside", it wrote outside the destination; "timeout", it did not
    finish; "crash", a signal killed it, or it crashed, as the caller judges; "rejected", it exited
    with another status than 0; "expected", it extracted the expected tree; or "other", it extracted
    another tree, or any tree of a case to reject."""
    if outside:
        return "outside"
    if status is None:
        return "timeout"
    if crashed or status < 0:
        return "crash"
    if status:
        return "rejected"
    if case["verdict"] != "reject" and same(tree, expected_tree(case)):
        return "expected"
    return "other"


def problems(case, status, tree, outside=None):
    """Why a run fails the case, or [] if it passes. The status is 0 if the run extracted the archive,
    positive if it rejected it, negative if a signal killed it, and None if it did not finish; tree
    is what it extracted, as walk gives it, and outside what it wrote outside the destination."""
    kind = classify(case, status, tree, outside)
    if kind == "outside":
        return [f"writes outside the destination: {path}" for path in sorted(outside)]
    if kind == "timeout":
        return [f"does not finish within {TIMEOUT} seconds"]
    if kind == "crash":
        return [f"killed by {signal.Signals(-status).name}"]
    if kind == "rejected":
        return ["rejects a case to accept"] if case["verdict"] == "accept" else []
    if kind == "expected":
        return []
    if case["verdict"] == "reject":
        return ["accepts a case to reject"]
    expected = expected_tree(case)
    out = []
    for path in sorted(set(tree) | set(expected)):
        if path not in tree:
            out.append(f"missing {path!r}: {json.dumps(expected[path], sort_keys=True)}")
        elif path not in expected:
            out.append(f"extra {path!r}: {json.dumps(tree[path], sort_keys=True)}")
        elif any(tree[path].get(k) != v for k, v in expected[path].items()):
            out.append(f"{path!r} is {json.dumps(tree[path], sort_keys=True)}, "
                       f"not {json.dumps(expected[path], sort_keys=True)}")
    return out


def shorten(message, limit=300):
    """A message cut after about limit characters: it comes first, and what follows is where it was
    raised."""
    return message if len(message) <= limit else message[:limit].rsplit(None, 1)[0] + " …"


def load_cases():
    """The cases, {name: case}, by identifier."""
    cases = {}
    for name in sorted(os.listdir(ARCHIVES)):
        if name.endswith(".json"):
            with open(os.path.join(ARCHIVES, name)) as f:
                cases[name[:-5]] = json.load(f)
    return dict(sorted(cases.items(), key=lambda kv: kv[1]["id"]))


def main():
    args = sys.argv[1:]
    i = args.index("--") if "--" in args else len(args)
    options, argv = args[:i], args[i + 1:]
    if not argv:
        sys.exit(__doc__.split("\n\n")[1])
    ids = set()
    while options:
        if options[0] != "--case" or len(options) < 2:
            sys.exit(f"{options[0]}: expected --case ID")
        ids.update(i.strip() for i in options[1].split(",") if i.strip())
        options = options[2:]
    if os.path.lexists(ABSOLUTE):
        sys.exit(f"{ABSOLUTE} exists, and would count as written by the first case: remove it first")
    cases = load_cases()
    unknown = ids - {case["id"] for case in cases.values()}
    if unknown:
        sys.exit(f"no such cases: {' '.join(sorted(unknown))}")
    if ids:
        cases = {name: case for name, case in cases.items() if case["id"] in ids}

    def command(archive, dest):
        return [a.replace("{archive}", archive).replace("{dest}", dest) for a in argv]

    failed = 0
    for name, case in cases.items():
        with tempfile.TemporaryDirectory() as root:
            status, out, err, tree, outside = extract(command, os.path.join(ARCHIVES, name + ".tar"), root)
        found = problems(case, status, tree, outside)
        failed += bool(found)
        did = "" if found else "rejects it" if status else "extracts the expected tree"
        print(f"{name:<45} {case['verdict']:<9} {'FAIL' if found else 'ok':<4} {did}".rstrip())
        for line in found:
            print("    " + line)
        message = err.strip() or out.strip()
        if status and message:
            print(textwrap.indent(shorten(message), "    "))
    print(f"{failed} of {len(cases)} cases fail")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()

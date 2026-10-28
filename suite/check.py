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
problems(case, rejected, walk(dest)), which is empty if the case passes.

It needs nothing outside suite/ but the Python standard library.
"""

import hashlib
import json
import os
import shutil
import stat
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ARCHIVES = os.path.join(HERE, "archives")
TIMEOUT = 60
# The absolute name of N12: in /tmp, which an extractor that follows it can write without root
ABSOLUTE = "/tmp/tar-minefield-absolute"


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


def extract(command, archive, root, timeout=TIMEOUT):
    """Run command(archive, dest), which extracts archive into dest, root/x/y/dest. Return (status,
    stdout, stderr, tree, outside), where status is None if it does not finish within timeout, and
    outside is what was written in root but not under dest, or at ABSOLUTE, which is removed."""
    dest = os.path.join(root, "x", "y", "dest")
    os.makedirs(dest)
    with open(archive, "rb") as stdin:
        try:
            p = subprocess.run(command(archive, dest), cwd=dest, stdin=stdin, capture_output=True,
                               timeout=timeout)
            code, out, err = p.returncode, p.stdout.decode(errors="replace"), p.stderr.decode(errors="replace")
        except subprocess.TimeoutExpired:
            code, out, err = None, "", "timeout"
    tree = walk(dest, dest)
    outside = {p: e for p, e in walk(root, dest).items()
               if p not in ("x", "x/y", "x/y/dest") and not p.startswith("x/y/dest/")}
    if os.path.lexists(ABSOLUTE):
        outside[ABSOLUTE] = entry(ABSOLUTE)
        if os.path.isdir(ABSOLUTE) and not os.path.islink(ABSOLUTE):
            shutil.rmtree(ABSOLUTE)
        else:
            os.remove(ABSOLUTE)
    return code, out, err, tree, outside


def problems(case, rejected, tree, outside=None):
    """Why an extraction fails the case, or [] if it passes. The tree is what was extracted, as walk
    gives it, and outside what was written outside the destination."""
    if outside:
        return [f"writes outside the destination: {path}" for path in sorted(outside)]
    if case["verdict"] == "reject":
        return [] if rejected else ["accepts a case to reject"]
    if rejected:
        return [] if case["verdict"] == "tolerate" else ["rejects a case to accept"]
    expected = expected_tree(case)
    if same(tree, expected):
        return []
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
    if "--" not in args or args.index("--") == len(args) - 1:
        sys.exit(__doc__.split("\n\n")[1])
    options, argv = args[:args.index("--")], args[args.index("--") + 1:]
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

    def command(archive, dest):
        return [a.replace("{archive}", archive).replace("{dest}", dest) for a in argv]

    failed = 0
    for name, case in cases.items():
        if ids and case["id"] not in ids:
            continue
        with tempfile.TemporaryDirectory() as root:
            code, out, err, tree, outside = extract(command, os.path.join(ARCHIVES, name + ".tar"), root)
        if code is None:
            found = [f"does not finish within {TIMEOUT} seconds"]
        elif code < 0:
            found = [f"killed by signal {-code}"]
        else:
            found = problems(case, code != 0, tree, outside)
        did = "rejects it" if code else "extracts the expected tree"
        failed += bool(found)
        print(f"{name:<45} {case['verdict']:<9} {'FAIL' if found else 'ok':<4} {'' if found else did}".rstrip())
        for line in found:
            print("    " + line)
        if code:
            lines = (err.strip() or out.strip() or f"status {code}").splitlines()
            # the error of a Python traceback is its last line
            message = lines[-1] if lines[0].startswith("Traceback") else lines[0]
            print("    " + message.replace(root, "ROOT"))
    print(f"{failed} of {len(ids) or len(cases)} cases fail")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()

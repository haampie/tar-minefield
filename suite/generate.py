"""Write the archives of the test suite from the scripts in cases/, and check them.

    python -I suite/generate.py            # write archives/
    python -I suite/generate.py --check    # fail if archives/ is not what the scripts write

For each case `<case>.py`, named by its identifier, such as `F15-pax-size-on-dir.py`, archives/ has
`<case>.tar`, the dump of its blocks `<case>.txt`, a map of them `<case>.svg`, and `<case>.json`:
its identifier, its verdict, the features of tarscan.py that it is about, and for the cases to accept
and the tolerated ones the tree an implementation must extract. Generation is deterministic.

A case is a script in cases/, named by its identifier, the next free number of its letter, and a few
words. It defines `ID`; `VERDICT`, one of "reject", "accept" and "tolerate"; `FEATURES`; `TREE`,
unless it is to reject; and `build(archive)`, which writes the archive with blocks.py. Its docstring
explains the case: first what is in the archive, in a paragraph that cites nothing, then the
decision point where implementations differ, where the scans saw it, and what implementations do
with it. Where it relies on a sentence of POSIX, it links words to it as `[words][key]`, by its key
in contrib/citations.py, which the site makes a link; in archives/, they are the words alone. It
stands on its own: other cases are named only in its `See also:` lines.

It needs nothing outside suite/ but the Python standard library.
"""

import hashlib
import importlib.util
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from blocks import Archive, block_map  # noqa: E402

CASES = os.path.join(HERE, "cases")
ARCHIVES = os.path.join(HERE, "archives")
VERDICTS = {"reject": "must reject",
            "accept": "must accept, and extract its tree",
            "tolerate": "tolerated: a strict parser may reject it; if it accepts it, it must extract its "
                        "tree, and the default policy accepts it"}


def load(path):
    spec = importlib.util.spec_from_file_location(os.path.basename(path)[:-3], path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def tree(entries):
    """The tree of a case as data: contents as their size and sha256."""
    out = []
    for e in entries:
        e = dict(e)
        if "contents" in e:
            contents = e.pop("contents")
            e["size"] = len(contents)
            e["sha256"] = hashlib.sha256(contents).hexdigest()
        out.append(e)
    return out


def plain(text):
    """Text with its links to sentences of POSIX, `[words][key]`, as the words."""
    return re.sub(r"\[([^\[\]]+)\]\[[a-z0-9-]+\]", r"\1", text)


def generate():
    """{file name: bytes} of every case."""
    files, ids = {}, {}
    for name in sorted(os.listdir(CASES)):
        if not name.endswith(".py"):
            continue
        case = name[:-3]
        module = load(os.path.join(CASES, name))
        assert re.fullmatch(r"[FNKS]\d\d", module.ID), f"{case}: an identifier such as F01"
        assert case.startswith(module.ID + "-"), f"{case}: the name starts with its identifier"
        assert module.VERDICT in VERDICTS, f"{case}: a verdict of {sorted(VERDICTS)}"
        assert module.ID not in ids, f"{case}: the identifier of {ids.get(module.ID)}"
        assert not re.search(r"\]\[[a-z0-9-]+\]", module.__doc__.strip().split("\n\n")[1]), \
            f"{case}: the first paragraph says what is in the archive, and cites nothing"
        others = set(re.findall(r"\b[FNKS]\d\d\b", "\n".join(
            line for line in module.__doc__.split("\n") if not line.startswith("See also:"))))
        assert others <= {module.ID}, f"{case}: names {sorted(others - {module.ID})} outside See also"
        ids[module.ID] = case
        archive = Archive()
        module.build(archive)
        expected = {
            "id": module.ID,
            "verdict": module.VERDICT,
            "description": plain(module.__doc__.strip().split("\n")[0]),
            "features": getattr(module, "FEATURES", []),
        }
        if module.VERDICT != "reject":
            expected["tree"] = tree(module.TREE)
        header = f"{case}: {VERDICTS[module.VERDICT]}\n\n{plain(module.__doc__.strip())}\n\n"
        files[f"{case}.tar"] = archive.bytes()
        files[f"{case}.txt"] = (header + archive.dump()).encode()
        files[f"{case}.svg"] = block_map(
            archive, f"{case}: every block of the archive").encode()
        files[f"{case}.json"] = (json.dumps(expected, indent=1) + "\n").encode()
    return files


def main():
    args = sys.argv[1:]
    files = generate()
    if "--check" in args:
        on_disk = set(os.listdir(ARCHIVES)) if os.path.isdir(ARCHIVES) else set()
        differ = [n for n in sorted(files) if n not in on_disk
                  or open(os.path.join(ARCHIVES, n), "rb").read() != files[n]]
        extra = sorted(on_disk - set(files))
        for n in differ:
            print(f"archives/{n}: not what the scripts write")
        for n in extra:
            print(f"archives/{n}: no script writes it")
        if differ or extra:
            sys.exit(1)
    else:
        os.makedirs(ARCHIVES, exist_ok=True)
        for n, data in files.items():
            with open(os.path.join(ARCHIVES, n), "wb") as f:
                f.write(data)


if __name__ == "__main__":
    main()

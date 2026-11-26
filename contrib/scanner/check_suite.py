"""Check the scanner and the default policy against the test suite.

    python -I contrib/scanner/check_suite.py

Every case must make tarscan.py report its features. The default policy of strict.py must reject
the cases to reject, accept the tolerated cases only by its rules, and accept the cases to accept
without them. And the letter of the identifier of a case must be the category of its features.
That tests the scanner and the policy against cases defined by their bytes, which a reviewer checks
by reading the scripts and dumps of suite/.

Every feature that tarscan.py reports of the cases, and of the pax records in RECORDS, in local and
global headers, must be classified by strict.py, so that the default policy accepts none unseen.
"""

import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import strict  # noqa: E402
import tarscan  # noqa: E402

ARCHIVES = os.path.join(HERE, "..", "..", "suite", "archives")
# The data of pax headers with every problem of records that tarscan.py reports
RECORDS = [
    b"x",
    b"015 path=evil\n",
    b"14 path =evil\n",
    b"13 path=evil\n\0\0\0",
    b"12 path=evil",
    b"9 =value\n",
    b"11 novalue\n",
    b"8 path=\n",
    b"10 key=\xff\xfe\n",
    b"15 comment=a\nb\n",
    b"12 path=a\0b\n",
    b"11 path=ab\n11 path=cd\n",
    b"9 size=0\n9 size=1\n",
    b"11 pa\0th=a\n",
]


def check():
    """Problems with what tarscan.py and the default policy make of the cases."""
    problems = []
    for name in sorted(os.listdir(ARCHIVES)):
        if not name.endswith(".tar"):
            continue
        case = name[:-4]
        with open(os.path.join(ARCHIVES, f"{case}.json")) as f:
            expected = json.load(f)
        with open(os.path.join(ARCHIVES, name), "rb") as f:
            r = tarscan.scan(io.BytesIO(f.read()))
        found = set(r["features"])
        unclassified = sorted(f for f in found if strict.classify(f)[0] == "unclassified")
        if unclassified:
            problems.append(f"{case}: strict.py does not classify {unclassified}")
        missing = set(expected["features"]) - found
        if missing:
            problems.append(f"{case}: tarscan.py does not report {sorted(missing)}")
        strict_found, rejected = strict.strict_features(r), strict.default_rejects(r)
        verdict = expected["verdict"]
        if verdict == "reject" and not rejected:
            problems.append(f"{case}: the default policy accepts it ({sorted(found)})")
        if verdict == "tolerate" and (rejected or not strict_found):
            problems.append(f"{case}: not accepted by a rule of the default policy: rejects "
                            f"{sorted(rejected)}, strict {sorted(strict_found)}")
        if verdict == "accept" and strict_found:
            problems.append(f"{case}: a strict criterion rejects it: {sorted(strict_found)}")
        categories = {strict.classify(f)[1] for f in expected["features"]} - {None} or {"framing"}
        category = strict.CATEGORIES["FNKS".index(expected["id"][0])]
        if verdict != "accept" and category not in categories:
            problems.append(f"{case}: the identifier {expected['id']} is not of the category {categories}")
        print(f"{case}: {sorted(found)}")
    for kind in ("pax", "pax-global"):
        for data in RECORDS:
            features = tarscan.Features()
            tarscan.pax_records(data, features, kind)
            unclassified = sorted(
                f for f in features.counts if strict.classify(f)[0] == "unclassified")
            if unclassified:
                problems.append(f"{kind} records {data!r}: strict.py does not classify {unclassified}")
    return problems


def main():
    problems = check()
    for p in problems:
        print(p)
    if problems:
        sys.exit(1)


if __name__ == "__main__":
    main()

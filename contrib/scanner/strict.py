"""How many real tarballs a strict parser would reject, as Markdown.

    python -I contrib/scanner/strict.py RESULTS... > STRICT.md
    python -I contrib/scanner/strict.py --readme README.md RESULTS...

A strict parser rejects every archive with a feature that METHOD.md lists as an ambiguity: the
criteria below, each a pattern of feature names of tarscan.py. Features of the cases that
METHOD.md lists to accept, or that are confined to fields outside the tree it describes, are
allowed. Names that some filesystems do not allow (`platform.*`) are neither: they are reported
apart. A feature that none of these patterns match is reported as unclassified, so that nothing is
left out unseen.

The default policy, `DEFAULT`, is what METHOD.md decides from these scans: it normalizes some of
the criteria and accepts others, and rejects the rest. What each rejects is given of both.

Each results file is the scan of an ecosystem, and rates are given per ecosystem: each is a
sample of its own population. Files of which tarscan.py cannot read the first header are not
assessed, as no implementation extracts anything from them: tarballs in a compression that it does
not read, such as lzip and zstd, and files that are no tar archive, such as a zip named .tar.gz.

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
import tarscan  # noqa: E402
from report import ecosystems, load, origin, tidy_tables  # noqa: E402

SITE = "https://stoppels.ch/tar/"

CATEGORIES = ("framing", "name", "kind", "order and state")

# (pattern, category, what it means), in order: the first pattern that matches a feature applies.
STRICT = [
    ("scan.error", "framing", "the scanner could not read past a header"),
    ("checksum.*", "framing", "a checksum that matches only one way of summing"),
    # Numeric fields that shape the tree are one criterion per problem: see criterion()
    ("number.[*].*", "framing",
     "a numeric field written in a way that implementations differ on"),
    ("number.size.*", "framing", "a size written in a way that implementations differ on"),
    ("number.chksum.*", "framing",
     "a checksum field written in a way that implementations differ on"),
    ("number.uid.*", "framing",
     "a uid that is not a number, at which some implementations end the archive"),
    ("number.gid.*", "framing",
     "a gid that is not a number, at which some implementations end the archive"),
    ("number.mtime.*", "framing",
     "an mtime that is not a number, at which some implementations end the archive"),
    ("magic.posix-version-nuls", "framing", "POSIX magic with NULs as its version"),
    ("magic.posix-with-odd-version", "framing", 'POSIX magic with a version other than `"00"` or NULs'),
    ("magic.*", "framing", "a header that implementations may not recognize as one"),
    ("type.unknown-*", "framing", "an unknown typeflag: data or no data"),
    ("type.gnu-sparse", "framing", "GNU's old sparse files"),
    ("type.contiguous", "framing", "contiguous files (7)"),
    ("type.fifo", "kind", "a FIFO, which the tree does not have: created, an empty file, or left out"),
    ("type.chardev", "kind", "a character device, which the tree does not have"),
    ("type.blockdev", "kind", "a block device, which the tree does not have"),
    ("pax.invalid-size", "framing", "a pax size that is not a number"),
    ("pax.size-leading-zero", "framing",
     "a pax size with leading zeros, which a reader may take as octal"),
    ("pax.size-too-large", "framing",
     "a pax size of 2^63 or more, which readers wrap, cut or reject"),
    ("pax.size-on-*", "framing", "a pax size on a member without data"),
    ("pax.size-repeated", "framing", "a pax size twice in one header: the first, or the last"),
    ("pax.SCHILY.realsize", "framing",
     "star's size of a sparse file, which libarchive cuts the data of any file to"),
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
    ("pax.nul-in-key", "framing",
     "a NUL in a pax key, at which some implementations end the records"),
    ("pax.empty-value.size", "framing", "an empty pax size, which in POSIX removes it"),
    ("pax-global.empty-value.size", "framing",
     "an empty size in a global header, which in POSIX removes the size of every later member"),
    ("pax*.value-not-utf8.comment", "framing", "a comment that is not UTF-8"),
    ("format.pax-after-v7", "framing",
     "pax headers after a v7 header, which a reader that takes the format of the first header "
     "extracts as files"),
    ("end.missing", "framing", "no end-of-archive marker"),
    ("end.unpadded", "framing", "an archive that ends before the data of its last member is "
                                "padded to a block"),
    ("end.lone-zero-block", "framing", "an end-of-archive marker of one zero block, not two"),
    ("end.data-after", "framing", "data other than zeros after the end-of-archive marker"),
    ("end.archive-after", "framing", "another archive after the end-of-archive marker"),
    ("end.zero-block-before-member", "framing", "a zero block, then more members"),
    ("end.*", "framing", "the end of the archive"),
    ("archive.empty", "framing", "no members at all"),
    ("name.leading-dot-slash", "name", "a name like `./a`, which some implementations make `a`"),
    ("name.dot", "name", "a member named `.` or `./`"),
    ("name.dot-on-*", "kind",
     "a member named `.` that is not a directory: the root of the tree as a file or link, or dropped"),
    ("name.dot-component", "name", "a name like `a/./b`"),
    ("name.double-slash", "name", "a name like `a//b`"),
    ("name.trailing-slash-on-file", "kind", "a regular file named like a directory, `a/`"),
    ("name.trailing-slash-on-*", "kind", "a link whose name ends in a slash"),
    ("name.trailing-dot-on-*", "kind",
     "a member that is not a directory whose name ends in `/.`, which is a directory"),
    ("name.absolute", "name", "an absolute name"),
    ("name.dotdot", "name", "a name with `..`"),
    ("name.empty", "name", "an empty name"),
    ("name.backslash", "name", "a backslash, `\\`, which is a separator on Windows"),
    ("name.drive-letter", "name", "a drive letter"),
    ("name.control-character", "name", "a control character in a name"),
    ("name.not-utf8", "name", "a name that is not UTF-8"),
    ("linkname.not-utf8", "name", "a link target that is not UTF-8"),
    ("name.bytes-after-nul", "name", "bytes after the NUL that ends a name"),
    ("linkname.bytes-after-nul", "name", "bytes after the NUL that ends a link target"),
    ("gnu-long.empty", "name", "an empty GNU long name or link: the field in the header, or none"),
    ("gnu-long.no-nul", "name",
     "a GNU long name or link whose size leaves out its NUL: it ends at the size, or at a NUL after"),
    ("gnu-long.nul-inside", "name", "bytes after the NUL that ends a GNU long name or link"),
    ("name.*", "name", "a name that implementations may normalize differently"),
    ("extended.name-dotdot", "name",
     "an extended header whose own name has `..`: a reader that does not know its typeflag "
     "extracts it as a file of that name"),
    ("extended.linkpath-on-*", "kind",
     "a link target in an extended header of a member that is not a link"),
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
    ("pax.mode", "kind",
     "a pax `mode`, which is not a keyword of POSIX: ignored, or the mode of the member"),
    ("pax.acl", "kind",
     "an ACL in a pax header, which decides whether a file is executable where it is applied"),
    ("linkname.on-*", "kind", "a link target on a member that is not a link"),
    ("number.mode.*", "kind", "a mode written in a way that implementations differ on"),
    ("tree.duplicate.file-file", "order and state", "the same file twice"),
    ("tree.duplicate.*", "order and state", "one path as two members"),
    ("tree.under-*", "order and state", "a member under a file"),
    ("tree.through-symlink", "order and state", "a member written through a symlink"),
    ("tree.*", "order and state", "members that interact"),
    ("hardlink.to-itself", "order and state", "a hardlink to itself"),
    ("hardlink.absolute", "order and state",
     "a hardlink to an absolute path: the member of that name without the slash, or the file "
     "outside the destination"),
    ("hardlink.to-symlink", "order and state", "a hardlink to a symlink"),
    ("hardlink.target-trailing-slash", "order and state",
     "a hardlink to a file, spelled with a trailing slash or `/.`, which is a directory"),
    ("hardlink.mode-differs", "order and state",
     "a hardlink whose mode is executable and whose target's is not, or the reverse: one file "
     "with two modes"),
    ("hardlink.*", "order and state", "a hardlink to a later member, no member, or a misspelling"),
    ("pax-global.*", "framing",
     "records of a global header that implementations may split differently"),
]

ALLOWED = [
    ("name.fills-field", "a name of exactly 100 bytes, without NUL"),
    ("linkname.no-nul", "a linkname of exactly 100 bytes, without NUL"),
    ("name.non-ascii", "UTF-8 names"),
    ("name.not-nfc", "names not in NFC: one tree, whose names macOS may normalize"),
    ("name.dir-without-trailing-slash", "a directory without a trailing slash: the typeflag says"),
    ("ustar.prefix", "the ustar prefix field"),
] + [
    (f"number.{field}.{how}", "outside the tree" + (", and read alike" if alike else ""))
    for field in ("uid", "gid", "mtime")
    for how, alike in (("no-digits", True), ("no-terminator", True), ("leading-space", True),
                       ("base256", True), ("base256-negative", False),
                       ("base256-too-large", False))
] + [
    ("type.nul", "the typeflag NUL of regular files, from before POSIX"),
    ("v7.bytes-after-linkname", "bytes in fields that v7 headers do not use"),
    ("tree.dir-after-contents", "directories after their contents"),
    ("tree.duplicate.dir-dir", "the same directory twice"),
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
    ("pax.newline-in-value.comment",
     "a comment with newlines, since pax records are delimited by their length"),
]

# The default policy: the strict criteria that it lets through, and how; it rejects the others.
# A strict parser normalizes these names to the path they refer to, which is what tarscan.py
# compares to find duplicates, so normalizing hides none. The rest it accepts as they are, some
# only if condition() is true. The first rule that matches a criterion applies, and one that
# rejects makes an exception to a rule after it.
DEFAULT = [
    ("name.leading-dot-slash", "normalize", "`./a` is `a`"),
    ("name.dot", "normalize", "`.` is the root of the tree"),
    ("name.dot-component", "normalize", "`a/./b` is `a/b`"),
    ("name.double-slash", "normalize", "`a//b` is `a/b`"),
    ("hardlink.target-spelled-differently", "normalize", "a hardlink to `./a` is one to `a`"),
    ("symlink.absolute", "accept",
     "the symlink is created as it is, and writing through a symlink is rejected"),
    ("symlink.escapes", "accept",
     "the symlink is created as it is, and writing through a symlink is rejected"),
    ("end.data-after", "accept", "junk after the two zero blocks is ignored"),
    ("end.missing", "accept", "implementations that extract it extract the same tree"),
    ("pax-global.after-members", "accept", "only if every global header has only a `comment`"),
    ("magic.posix-version-nuls", "accept", 'some Java archivers write `"ustar\\0\\0\\0"`'),
    ("name.control-character", "accept",
     "the name is created as it is, as every implementation reads it alike, and the risk is in "
     "its use"),
    ("number.*.leading-space", "accept", "implementations read octal padded with spaces alike"),
    ("number.mode.base256*", "reject",
     "a mode fits in octal, and of the readers of base-256 some do not read a mode in it"),
    ("number.*.base256", "accept",
     "a reader that does not support base-256 cannot take it for octal, so it has one reading"),
    ("type.contiguous", "accept",
     "the file is extracted as a regular file, as POSIX asks of implementations without "
     "contiguous files"),
    ("pax.size-disagrees", "accept",
     "the pax size frames the member, as in POSIX, and is how sizes of 8 GiB and over are "
     "written"),
    ("pax*.value-not-utf8.comment", "accept",
     "a comment is ignored, so a reader need not decode it to check its encoding"),
    ("pax.newline-in-value.SCHILY.xattr.*", "accept", "xattrs are not extracted"),
    ("pax.newline-in-value.LIBARCHIVE.xattr.*", "accept", "xattrs are not extracted"),
]

@functools.cache
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
    """Whether tarscan.py read the tarball: not if it failed at the first header, as it does on a
    compression that it does not read, which it takes for an uncompressed tar."""
    return "features" in r and not (r.get("error") and not r.get("members"))


def criterion(feature):
    """The criterion of a strict feature: a problem of numeric fields is one criterion for all of
    them, as a strict parser has one rule for it. A mode in base-256 is a criterion of its own, as
    the default policy accepts base-256 in the other fields, where it is written."""
    if feature.startswith("number.mode.base256"):
        return feature
    return re.sub(r"^number\.(size|mode|chksum|uid|gid|mtime)\.", "number.*.", feature)


def strict_features(r):
    found = {criterion(f) for f in r["features"] if classify(f)[0] == "strict"}
    if r.get("error") or r.get("compression_error") or r.get("compression", {}).get("truncated"):
        found.add("scan.error")
    return found


def default_rule(feature):
    """The rule of DEFAULT for a strict feature: (pattern, how, why), or None if rejected, as it is
    by no rule, or by one that makes an exception to a later rule."""
    for rule in DEFAULT:
        if fnmatch.fnmatchcase(feature, rule[0]):
            return rule if rule[1] != "reject" else None
    return None


def condition(feature, r):
    """Whether the conditions of DEFAULT are met for a feature that it accepts, from what the
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
    return may | may_have_7078a34ab512(r)


def may_have_7078a34ab512(r):
    """The features of UNREPORTED that a tarball that version 7078a34ab512, or an earlier one,
    scanned may have: pax headers after a v7 header if it has both, a link target that is not
    UTF-8 if it has links, as no version recorded the bytes of link targets, a member that is not a
    directory with a name that is the root, such as `.` or `./.`, if it has one of the names that
    those give and members that are not directories, and a hardlink to an absolute path if it has
    hardlinks and a hardlink feature or an absolute name, as their targets were normalized. And
    the features of LATER_2: see may_have_later_2."""
    fingerprint, kinds, features = r.get("fingerprint", {}), r.get("kinds", {}), r["features"]
    may = may_have_later_2(r)
    root = "name.dot" in features or "name.absolute" in features or (
        "name.leading-dot-slash" in features and ("name.dot-component" in features or any(
            f.startswith("name.trailing-slash-on-") for f in features)))
    if root and any(k != "dir" for k in kinds):
        may.add("name.dot-on-*")
    if kinds.get("hardlink") and ("name.absolute" in features or any(
            f.startswith("hardlink.") for f in features)):
        may.add("hardlink.absolute")
    pax = any(t in s for s in fingerprint.get("extended_sequence", {}) for t in "xX")
    if fingerprint.get("magic", {}).get("v7") and (pax or fingerprint.get("pax_global_keys")):
        may.add("format.pax-after-v7")
    if kinds.get("symlink") or kinds.get("hardlink"):
        may.add("linkname.not-utf8")
    return may


def may_have_later_2(r):
    """The features of LATER_2 that a tarball may have, from what every version recorded of it.
    The kinds of its members say whether it has a FIFO or a device. Its data can end without
    padding only if it has no end-of-archive marker. Its pax keys and the shapes of its checksum
    fields are in its fingerprint, which keeps the 8 most common of each, so that a tarball with
    8 may have others. The name of an extended header is recorded with `*` for the components
    that are not its own, one of which may be `..`. A name that ends in `/.` has a `.` component,
    and a hardlink to a file spelled with a trailing slash is spelled differently, unless a member
    has that name. A member can be at the path of a directory that is not a member, and a hardlink
    can have another mode than its target, in any tarball that has such members."""
    fingerprint, kinds, features = r.get("fingerprint", {}), r.get("kinds", {}), r["features"]
    may = {f"type.{k}" for k in tarscan.SPECIAL if kinds.get(k)}
    may |= {f"tree.duplicate.dir-{k}" for k in kinds if k != "dir"}
    if "end.missing" in features:
        may.add("end.unpadded")
    for kind, keys in (("pax", fingerprint.get("pax_keys", {})),
                       ("pax-global", fingerprint.get("pax_global_keys", {}))):
        many = len(keys) >= 8
        if many or any("\0" in k for k in keys):
            may.add(f"{kind}.nul-in-key")
        if f"{kind}.repeated-key" in features and (many or "size" in keys):
            may.add(f"{kind}.size-repeated")
        if kind == "pax" and (many or "mode" in keys):
            may.add("pax.mode")
        if kind == "pax" and (many or any(k.endswith(".xattr.*") or k.startswith("SCHILY.acl.")
                                          for k in keys)):
            may.add("pax.acl")
    shapes = fingerprint.get("checksum", {})
    if len(shapes) >= 8:
        may |= {f"number.chksum.{how}" for how in ("leading-nul", "gap-in-digits",
                                                   "invalid-character")}
    may |= {f for shape in shapes for f in tarscan.checksum_features(shape)
            if f != "number.chksum.leading-space"}
    names = [n.split("/") for key in ("pax_header_name", "pax_global_header_name", "gnu_long_name")
             for n in fingerprint.get(key, {})]
    if any(".." in parts or "*" in parts for parts in names) or any(
            len(fingerprint.get(key, {})) >= 8
            for key in ("pax_header_name", "pax_global_header_name", "gnu_long_name")):
        may.add("extended.name-dotdot")
    if "name.dot-component" in features and any(k != "dir" for k in kinds):
        may.add("name.trailing-dot-on-*")
    if kinds.get("hardlink"):
        if kinds.get("file"):
            may.add("hardlink.mode-differs")
        if any(f == "hardlink.target-spelled-differently" or f == "name.dot-component"
               or f.startswith("name.trailing-slash-on-") for f in features):
            may.add("hardlink.target-trailing-slash")
    return may


# Versions of tarscan.py that did not report some features: (those features, and a function of a
# tarball that version scanned to the ones it may have). A tarball that may have none of them is
# measured for them all the same; the others are not, until they are scanned again.
# The features that the scanner reports since the cases of issue 50: no scan has them yet
LATER_2 = (["type.fifo", "type.chardev", "type.blockdev", "end.unpadded", "pax.mode", "pax.acl",
            "pax.size-repeated", "pax-global.size-repeated", "pax.nul-in-key",
            "pax-global.nul-in-key", "number.chksum.leading-nul", "number.chksum.gap-in-digits",
            "number.chksum.invalid-character", "extended.name-dotdot", "name.trailing-dot-on-*",
            "hardlink.target-trailing-slash", "hardlink.mode-differs"]
           + [f"tree.duplicate.dir-{k}" for k in ("file", "hardlink", "symlink") + tarscan.SPECIAL])
LATER = ["format.pax-after-v7", "linkname.not-utf8", "name.dot-on-*", "hardlink.absolute"] + LATER_2
UNREPORTED = {
    "25bfa32e6e71": (
        ["pax.empty-value.*", "pax-global.empty-value.*", "pax.value-not-utf8.*",
         "pax-global.value-not-utf8.*", "pax.size-leading-zero", "pax.size-too-large",
         "extended.gnu-long-and-pax", "number.*.base256-too-large"] + LATER,
        may_have_25bfa32e6e71,
    ),
    "5b9b83abac66": (LATER, may_have_7078a34ab512),
    "7078a34ab512": (LATER, may_have_7078a34ab512),
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
    """The bin of MTIME_BINS of a tarball by the median mtime of its members, "fixed" where that is
    one of fixed, as where cargo writes its mtime on all but a few members, and "unknown" where it
    is not after 1980."""
    m = r.get("mtime")
    if m and m[1] in fixed:
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
        "Fixed: the median mtime is one that a producer writes in place of the real one, such as "
        "`cabal sdist` (2001-09-09) on Hackage, hatchling (2020-02-02) on PyPI and cargo "
        f"(2006-07-24) on crates.io, so these tarballs are not dated: {dates}. Unknown: a median "
        "mtime not after 1980, such as the 1980-01-02 of RubyGems."
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
        f"[accepts {percent(len(union) - default, len(union))}]({SITE}#tarballs)."
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
        if how == "reject":
            continue
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
            "pax `size` does not have a pax size with a leading zero. `UNREPORTED` in "
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
            "Names that some filesystems do not allow, so that extraction fails there only: "
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

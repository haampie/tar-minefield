# Method

This document describes how tar-minefield decides which archives a strict tar parser must
reject, how it keeps that set small enough that strict parsers stay practical, and how its test
cases are produced so that anyone can audit them. It is a working draft.

## Terms

| term | meaning |
|---|---|
| **implementation** | A program or library that turns a tar archive into a tree, by extracting it or by listing its members: GNU tar, Python `tarfile`, Go `archive/tar`, … |
| **member** | One entry of an archive: a header, its extended headers, and its data. |
| **tree** | What an implementation extracts: paths, each with a kind (file, directory, symlink, hardlink), the contents of a file or the target of a link, and whether a file is executable. Nothing else, such as mtimes and owners. |
| **ambiguity** | Something in an archive from which two implementations, each following a defensible reading of POSIX, GNU tar or practice, extract different trees. |
| **category** | What an ambiguity changes in the tree, in no order: **F** framing, **N** names, **K** kinds, **S** order and state. |
| **strict parser** | An implementation that rejects an archive with an ambiguity, rather than extracting one of its trees. |
| **feature** | What the scanner reports of an archive, such as `name.leading-dot-slash`. |
| **criterion** | A feature that is an ambiguity, for which a strict parser may reject an archive. The [catalogue](#initial-catalogue) lists them. |
| **policy** | The criteria a strict parser rejects: either *every criterion*, or the [default policy](#the-default-policy). |
| **test suite** | The archives of [suite/](suite), each a case, for implementations to run against. |
| **identifier** | The permanent name of a case: the letter of its category and a number, such as `F15`. |
| **case** | An archive of the test suite, named by its identifier (its category and a number) and a few words, such as `F15-pax-size-on-dir`, with a verdict, and a manifest unless it is to reject. |
| **verdict** | What a case requires: **reject**, a strict parser must reject it; **accept**, every implementation must accept it; **tolerate**, a strict parser may reject it, and the default policy accepts it. See [Verdicts](#verdicts). |
| **manifest** | The tree an implementation must extract from a case to accept or a tolerated case, if it accepts it. |
| **outcome** | What an implementation makes of a case: ✅ as its verdict says, ⚠️ accepts a case to reject, ⛔ rejects a tolerated case, ❌ rejects a case to accept or extracts another tree than the manifest, 💥 writes outside its destination. |
| **tarball** | An archive released by a project and pinned by a package manager, as opposed to a case. |

## Goal

A test suite of tar archives, each with a verdict, that any tar implementation can run against: a
reference for what a strict parser rejects, what it must accept, and what it must make of the
archives it accepts.

The test suite is not limited to archives on which today's implementations disagree. Disagreement
between, say, GNU tar and Python's `tarfile` is evidence of an ambiguity, but an archive that every
known implementation interprets the same way can still be ambiguous: it only takes the next
implementation to make the other reasonable choice. The test suite records both.

## Scope

The tar layer only: the input is the decompressed byte stream. Ambiguities in compression
formats are real and interact with tar (see [Future work](#future-work)), but are out of scope for
now.

The interpretation that matters is the one relevant to distributing software. An archive maps to
a tree of entries, each with

- a path,
- a kind: regular file, directory, symlink or hardlink,
- the contents of a regular file, or the target of a link,
- whether a regular file is executable.

Fields outside this model (mtime, uid, gid, uname, gname, xattrs, device numbers, most of the
mode) are not restored by an extractor for software distribution, so an ambiguity confined to
them is harmless. Stating this up front is what keeps strictness in check: an implementation can be
strict about every field that shapes the tree and lenient about everything else.

## When an archive is ambiguous

An archive is ambiguous if two implementations, each following a defensible reading of POSIX, the
GNU tar documentation or long-standing practice, produce different trees from it. For each case we
name the *decision point*: the place in an implementation where implementations make different
choices. The verdict of the case says which of them a strict parser makes.

A case is ambiguous when it can be read in more than one way, whether or not the implementations
measured here differ: they can agree because they followed one, such as GNU tar, and an
implementation written later, or one that is refactored, need not.

Ambiguities fall into four categories, by what they change in the tree:

- **Framing**: where a member's data ends and the next header begins, and which headers belong to
  a member. An implementation that frames an archive differently sees different members, so whole
  files can be hidden from one implementation and visible to another.
- **Name**: which of several fields gives a member its path, and how a path is normalized.
- **Kind**: the mode of a member: file, directory, link or executable.
- **Order and state**: what happens when members interact, through duplicate paths or links.

### Initial catalogue

Framing:

- Number fields: a leading NUL (GNU tar skips it, `tarfile` stops at it), spaces or NULs
  between digits, no terminator, digits 8 and 9, an empty field, base-256 (positive and
  negative, and sizes past 64 bits, which some readers wrap around).
- Checksums: signed versus unsigned sums, and the formats of the checksum field.
- Sizes of members that carry no data in some implementations: directories, hardlinks, symlinks,
  devices, fifos.
- Unknown typeflags: POSIX treats them as regular files with data, an implementation may also skip
  them without data.
- GNU's old sparse (`S`), multivolume (`M`), volume label (`V`) and dumpdir (`D`) headers, and
  contiguous files (`7`).
- A pax `size` that disagrees with the header's size (POSIX says the pax size wins: it is how
  sizes over 8 GiB are written), a pax `size` on a member that has no data, and a pax `size`
  applied to an extended header rather than to the member, which is the bug class of
  CVE-2025-62518 (tokio-tar), GHSA-3pv8-6f4r-ffg2 (tar-rs) and CVE-2026-53655 (node-tar).
- pax numbers, which are ASCII decimal digits: a sign, leading whitespace, other digits of Unicode
  (which conversions of strings to numbers, such as Python's `int`, accept), leading zeros
  (decimal to POSIX, octal to `strtoul(s, NULL, 0)`), and values past 64 bits.
- Empty values in pax headers, which in POSIX remove a key: an empty `size` leaves a member
  without a size, which implementations take as 0, as the header's size, or reject.
- pax record framing: the length counts itself, leading zeros in the length, data after the last
  record, records not ending in a newline, values that contain a newline (records are delimited by
  length, so an implementation that splits on lines sees different records, even in a `comment`
  that no implementation applies), keys with whitespace (GNU tar strips it, `tarfile` does not).
- The end of the archive: a lone zero block, zero blocks followed by more members (GNU tar's
  `--ignore-zeros`), data other than zeros after the end-of-archive marker, no marker at all.
- Recognizing a header: v7 headers without magic, the POSIX magic `ustar\0` with the GNU version
  field and vice versa, damaged magic.
- Global pax headers: a `size` in one, one between an extended header and its member, which the
  extended header may apply to, and one after the first member, whose values apply to the members
  after it only.

Name:

- Several sources for one name: a pax `path`, a GNU long name (`L`), the ustar prefix and name,
  the star prefix, Solaris `X` headers, two extended headers of one kind, one key twice in an
  extended header, or one of each.
- GNU long names and pax headers for one member, in either order: each extends the next header,
  and does not know the other, so a GNU long name before a pax header may name the pax header.
- The prefix field in a header with GNU magic, which GNU tar uses for times in incremental
  archives (`tarfile` reads it as a prefix: gh-155629).
- pax keys that change the name or kind from inside: `GNU.sparse.name`, `SCHILY.filetype`.
- NUL inside a pax path or GNU long name, and GNU long names padded with NULs or spaces.
- `hdrcharset=BINARY`, names that are not UTF-8, and other pax values that are not UTF-8, which
  POSIX does not allow, but libarchive and star write xattrs as.
- An empty pax `path` or `linkpath`, which in POSIX removes it, rather than falling back to the
  header's name.
- Normalization: `./a` and `a`, `a//b`, `a/./b`, a trailing slash, `.`, an empty name, `\` as a
  separator on Windows, drive letters.
- The same questions for link targets: `linkpath`, GNU long links (`K`) and the linkname field.
- A `path` or `linkpath` in a global pax header, and empty values in one, which in POSIX remove an
  earlier global value.

Kind:

- A regular file whose name ends in a slash: the historical convention for directories. GNU tar
  1.35, `tarfile` and Ubuntu's patched GNU tar 1.35 make three different trees of one archive.
- A trailing slash on the name of a link.
- A link target in the linkname field of a member that is not a link.

Order and state:

- Duplicate paths: file and file (last wins, or first wins), file and directory, directory and
  directory, symlink and file (replace the symlink, or write through it).
- Writing through a symlink: a member `a/b` after a symlink `a`.
- Hardlinks to a later member, to a member that does not exist, to a directory, to a symlink (link
  the symlink or its target), to themselves, or to a target spelled differently from the member
  it names (`./a` and `a`).

## Verdicts

Every case has one of three verdicts, which are the `n_`, `y_` and `i_` of Nicolas Seriot's
JSONTestSuite:

- **reject**: a strict parser must reject it.
- **accept**: every implementation must accept it, and extract the tree in its manifest.
- **tolerate**: ambiguous in principle, but common enough in real archives that rejecting it has
  a real cost. A strict parser may reject it; if it accepts it, it must extract the tree in its
  manifest.

The cases to accept are as important as the cases to reject: without them, an implementation
that rejects everything passes. They cover what real archives contain and what a careless strict
parser would trip over:

- the global pax header with only a `comment` that `git archive` writes, and so every GitHub
  release tarball,
- pax headers for long names and links, GNU long names and links, and the ustar prefix,
- names of exactly 100 bytes, with no NUL,
- number fields padded with leading zeros or leading spaces, and terminated by a space, a NUL,
  or both, the checksum too: many CPAN tarballs, and those of old GNU tar, pad with spaces, and
  [the scans](contrib/data) find no tarball where implementations read such a field differently,
- base-256 sizes of files over 8 GiB,
- vendor pax keys that do not affect the tree, such as `LIBARCHIVE.xattr.*` and `SCHILY.*` from
  macOS and star, also with values that are not UTF-8, and the AppleDouble `._` files next to
  them,
- directories after their contents, and parent directories that have no member of their own,
- the same directory listed twice, as `tar cf x.tar dir dir/sub` writes.

Each case also records what is known about it:

- **observed**: implementations disagree today, with their names and versions,
- **historical**: implementations disagreed, and one was changed (for example gh-155629),
- **latent**: no known implementations disagree, with an argument why one could.

Whether an ambiguous case is rejected or tolerated is decided by measurement, as described
next. So a case is named by its identifier, such as `F15-pax-size-on-dir`, and not by its verdict,
which may change.

### The default policy

[The scans](contrib/data) decided it: the default policy rejects every case to reject, and accepts
the tolerated cases, which extract the tree in their manifest. Its table is `DEFAULT` in
`contrib/scanner/strict.py`, and [contrib/data/STRICT.md](contrib/data/STRICT.md) gives what it
costs. The tolerated cases are:

- names that refer to the same path, normalized to it: `./a` is `a`, `.` is the root, and
  `a/./b` and `a//b` are `a/b`. Duplicates are found among the normalized paths, so normalizing
  hides none.
- absolute symlinks, created as they are: the danger is in following them, and writing through
  any symlink is rejected.
- data after the end-of-archive marker that is not a header, which is ignored. A header there,
  another archive or members after a zero block, is rejected: some implementations extract them.
- a global pax header with only a `comment` after the first member.
- the POSIX magic with NULs for its version, `ustar\0\0\0`, which some Java archivers write,
  as in the tarballs of Apache's commons-lang, Solr and Hadoop. Any other version is rejected.
- newlines in the values of xattr pax keys, which are not extracted.
- a pax `size` that disagrees with the header's, when the pax size frames the member, as POSIX
  says. A strict parser may reject a header that could hold the size and gives another, but must
  not take the header's size.

Everything else in the catalogue is rejected. POSIX requires two zero blocks at the end of an
archive: a tar file that ends with a single zero block, or without any, is rejected, although most
implementations extract it. Duplicate files are rejected even where their copies are identical, as
they are in most tarballs that have them: in some, a file was changed and appended again, so that
implementations that keep the first copy and those that keep the last extract different trees. In
fish 4.7.1, `Cargo.toml` and `Cargo.lock` are appended again without their last newline; in
logstash 8.15.2, `build.rb` is a license header first and the build's date and commit last.

## Platform-specific failures

Whether an archive describes one tree, and whether a filesystem can hold that tree, are separate
questions. The first is about the archive, and its answer is the same on every platform. The
second is not:

- names that differ only in case (`INSTALL` and `install/`) are one entry on case-insensitive
  filesystems, the default on macOS and Windows,
- names that differ only in Unicode normalization are one entry on macOS,
- names that are reserved or invalid on Windows: `con`, `aux.c`, `nul.h`, `com1`, names with `:`
  or `"`, names ending in a dot or a space,
- symlinks, where a platform or user cannot create them.

Such an archive is not ambiguous: every implementation agrees on its tree, and an extractor that
never replaces an entry (`O_EXCL`) fails exactly on the filesystems that cannot hold it. So these
cases are to accept, with the platforms where extraction fails listed in their metadata, and a test
of them passes on those platforms when extraction fails without writing anything. A failure on one
platform does not carry over to another: a release tarball of an autotools project with a file
named `aux.c` is fine on Linux and macOS, and one that has `Foo` and `foo` is fine on Linux.

The scanner reports these names as `platform.*` features, apart from ambiguities, and
extraction failures that only the filesystem of the scanning machine causes are counted apart
from rejections.

## Not too strict: measuring real archives

A strict parser is useless if it rejects the tarballs people actually download. The question is
what fraction of real release tarballs each rule rejects, and the package repositories of Spack,
Nix and Guix answer it: each lists tens of thousands of tarballs, from decades of releases,
pinned by checksum.

### Sources

- Spack: the `builtin` repository has about 41,000 `sha256` checksums, of which some are patches
  and resources rather than tarballs. Spack's source mirror is content-addressed, at
  `https://mirror.spack.io/_source-cache/archive/<sha256[:2]>/<sha256>.<ext>`.
- Nix: `maintainers/scripts/find-tarballs.nix` in nixpkgs lists the tarballs of all packages, and
  `https://tarballs.nixos.org/sha256/<sha256>` serves them by checksum.
- Guix: `https://guix.gnu.org/sources.json` lists the sources of all packages with their
  checksums, for Software Heritage. Disarchive's database records the headers of the tarballs it
  can reassemble, which may allow some analysis without downloads.
- PyPI: the simple index lists the files of about a million projects, with their checksums, and
  `files.pythonhosted.org` serves them. Their sdists are millions, too many to scan, so a sample
  of projects is scanned, one sdist each: the latest of half, an older one of the other half.
- crates.io and RubyGems, sampled the same way: crates.io's index has the sha256 of every crate,
  which `cargo package` writes, and RubyGems' compact index that of every gem. A gem is a tar
  whose member `data.tar.gz` holds the files it installs, written by RubyGems itself: that member
  is the tarball measured, of gems for the platform `ruby`.

Tarballs are deduplicated by checksum, since the repositories overlap a lot, GNU releases
especially.

### A scanner, not an extractor

Running a dozen extractors over the test suite is slow, and makes every change of policy a new run.
Instead, a scanner reads only the headers of each tarball, skips the data, and records every
feature from the catalogue it finds, as one JSON line per tarball keyed by its checksum. It does
not stop at the first problem. A strictness policy is then a query over that table, and debating
it costs no downloads.

The scanner also records what identifies the producer of a tarball: the magic, how number fields
are padded, the `git archive` comment, uname and gname, the mtimes of the entries (which also date
the tarball). "Rule R rejects 0.4% of tarballs, all made by GNU tar 1.13 before 2004" is
actionable where "0.4%" is not.

### What to report

For each rule:

- the fraction of distinct tarballs it rejects,
- the fraction of packages with any version it rejects,
- the fraction of packages whose latest version it rejects, which is what decides whether a rule
  is practical,
- the producers and years of the tarballs it rejects.

The first run is on a sample of about 2,000 tarballs, stratified by repository and age.

### Who pays for ambiguity

Package managers that hash only the tarball (Spack, Guix's `url-fetch`, and about a quarter of
nixpkgs) are exposed to ambiguity silently: a different extractor gives different sources for the
same hash. Package managers that hash the extracted tree, such as Nix's `fetchzip`, see a
different interpretation as a hash mismatch: it breaks a build, but loudly. Those tree hashes are
also an oracle: extracting with a strict parser and comparing the hash checks its interpretation
against the one Nix recorded.

For the tarballs that are pinned by checksum, strictness can come with an allowlist: a reviewed
list of checksums, each with the hash of the tree it must extract to. Then the rare legacy
tarball keeps working, with its interpretation pinned, and a strict parser's cost is a one-time
review.

## Auditability

People should be able to trust the test suite without trusting its binary files.

- Every archive is produced by a small script that uses the Python standard library only, and
  builds the archive from raw 512-byte blocks with a short shared helper. Scripts never use
  `tarfile` or any other implementation under test: they normalize what they write, and the
  test suite would then test them against themselves. Each script explains its case in a docstring.
- Generation is deterministic: no clocks, no randomness, no dependency on the machine.
- The archives are checked into git, and CI regenerates them and fails on any difference. So
  every byte can be traced to a script that a reviewer can read.
- Next to each archive is a generated, annotated dump: every header block with its offset, its
  fields, their raw bytes and their meaning. A change to a case is then a readable diff.
- Expected trees are plain manifests (path, kind, sha256 of the contents, link target,
  executable), rather than a single hash.
- The interpretation of every case by every implementation we track (GNU tar, bsdtar, BusyBox,
  star, Python's `tarfile`, Go's `archive/tar`, Rust's `tar`, node-tar, 7-Zip, Apache Commons
  Compress, .NET's `System.Formats.Tar`, ...) is produced in CI at pinned versions, and published
  as data. Claims like "GNU tar does X" can then be checked by running them again.
- Cases are written from scratch, in our own words, also where they reproduce a known CVE: no
  archive or test is copied from another project.
- Payloads are harmless. Cases about traversal write marker files with obvious names, and the
  README warns that the test suite contains archives that escape their destination in lenient
  extractors.
- The table produced by the scanner is published too: anyone can download the same tarballs by
  checksum, check it, and apply their own policy.

## Trusting the tools

The generators and the scanner are themselves tools that read or write tar, written in Python,
and a reader may ask who checks them. The answer differs for each part, and in none of them is
it a single implementation that has to be taken on trust.

- **The test suite** is trusted for its bytes, not for its generators. A generator only writes
  bytes, and does not parse anything. Its output is checked into git with an annotated dump, and
  a reviewer can check both by hand against the case's description and the specification it
  cites. CI checks that the generators still produce exactly those bytes.
- **The verdicts** come from the specifications, the reasoning recorded with each case, and the
  interpretation matrix of real implementations, never from our scanner.
- **The scanner** is a measuring instrument: if it frames an archive differently from the
  implementations it stands in for, the statistics are wrong. So it is checked against them.
  For every tarball, it will record where each header starts and the name it gives the member,
  as one framing digest. GNU tar (`tar -tvR` prints the block of each header), bsdtar and
  `tarfile` (`TarInfo.offset`) can produce the same list. On the tarballs where they agree with
  each other, which is nearly all of them, they then check the scanner's framing, in two
  languages and three independent code bases. Where they disagree, the tarball is ambiguous,
  which is what we look for.
- **A second scanner** in another language, written from this document by someone who has not
  read `tarscan.py`, must produce the same output on the test suite and on real tarballs. Two
  independent implementations that agree catch what one implementation tested against itself
  cannot. It also suits the implementations we hope will run the test suite, many of which are in
  Go and Rust.
- **The test suite tests the scanner.** Every case to reject and every tolerated case must make the
  scanner report its feature, and every case to accept must make it report exactly the members in
  its manifest. That is
  not circular, because the cases are defined by reviewed bytes, not by the scanner's output.
  Differential fuzzing covers the rest: archives from a writer must be reported with exactly the
  members that were written.

Python is a deliberate choice, not a weakness to apologize for. It is memory-safe, while many
tar vulnerabilities were memory errors in C. Its integers do not overflow, which rules out a
class of tar bugs in sizes, base-256 numbers and sums of sizes. And it is easy to read, which
matters most for code that people are asked to audit. Its weaknesses here are speed, which does
not matter, and dynamic typing, which tests cover. The scripts use the standard library only, so
the code to trust is CPython and this repository. CPython's decompressors are C, but compression
is outside the scope, for now.

In the long run, the reference should be a document rather than code: a strict profile of tar,
with the rules for every header field and a grammar of pax records, cited by every case. Our
scripts and untar are then implementations of it, and agreement between them and an independent
implementation is the evidence that they are correct.

## Prior art

Test suites that became references for implementations, and how:

- [JSONTestSuite](https://github.com/nst/JSONTestSuite), from Nicolas Seriot's
  [Parsing JSON is a Minefield](https://seriot.ch/parsing_json.php): the `y_`/`n_`/`i_`
  verdicts and a published matrix of how each parser handles each case. Implementations such as
  [JSON-GLib](https://gitlab.gnome.org/GNOME/json-glib/-/merge_requests/63) and
  [Wuffs](https://skia.googlesource.com/external/github.com/google/wuffs/+/HEAD/script/run-json-test-suite.sh)
  run it.
- [x509-limbo](https://github.com/C2SP/x509-limbo): test vectors for X.509 path validation,
  generated by code, with results across implementations. Go's `crypto/x509` runs it in its own
  [tests](https://tip.golang.org/src/crypto/x509/x509limbo_test.go), with a justification for
  every case where it deliberately differs.
- html5lib-tests, toml-test, test262: suites shared by most implementations of their format.

Work on archives specifically:

- [My ZIP isn't your ZIP](https://www.usenix.org/conference/usenixsecurity25/presentation/you)
  (USENIX Security 2025) and its fuzzer [ZipDiff](https://github.com/ouuan/ZipDiff): 50 ZIP
  parsers, 14 types of ambiguity. It led to fixes such as uv's CVE-2025-54368.
- Michał Górny's [Portability of tar features](https://mgorny.pl/articles/portability-of-tar-features.html):
  which tar formats and features each implementation reads and writes. It is about portability,
  not ambiguity, and is from 2018.
- star's [`tartest`](https://freshports.org/archivers/tartest) and test archives, which check
  POSIX.1-1990 conformance. GNU tar can run star's archives in its
  [own tests](https://git.cworth.org/git/tar/tree/tests/star/README), disabled by default.
- The test suites of libarchive, GNU tar, Go's `archive/tar` and Python's `tarfile`, each written
  for one implementation.
- [Multi-interpretable tarballs](https://stoppels.ch/2026/10/22/multi-interpretable-tarballs.html),
  and [untar](https://github.com/haampie/untar), whose rules are the first candidate policy.

## Future work

- Compression formats: gzip files with several members, which some decoders stop after the first
  of; bzip2 and xz files with several streams; xz stream padding; zstd skippable frames; data
  after the compressed stream; gzip header CRCs and sizes. They interact with tar: a first stream
  that holds a complete archive, followed by a second stream that holds another, extracts
  differently depending on the decoder, unless the parser refuses data after the end-of-archive
  marker.
- Polyglots: files that are valid tar and valid ZIP, or tar and something else.
- Writers: which tools produce archives that strict parsers reject.

## Open questions

- Is a single verdict per case enough, or do some cases need a verdict per use (software
  distribution versus backups, where owners and modes matter)?
- Which normalizations of names are interpretation (`./a` is `a`) and which are a reason to
  reject? The default policy normalizes `./a`, `.`, `a/./b` and `a//b`, and rejects the rest.
- How should a rule that only old tarballs break be handled: tolerated, or rejected with an
  allowlist? The default policy rejects them, as the tarballs they reject are few: a package that
  needs one can allow it by the tarball's sha256.

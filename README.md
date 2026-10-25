# Tar file extraction test suite

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23617964.svg)](https://doi.org/10.5281/zenodo.23617964)

This repo provides an extensive **[test suite](suite/)** and **[documentation](https://stoppels.ch/tar/)** for tar file extraction, with the goal to ensure implementations extract tar archives the same way.

There are dozens of implementations of tar file extraction out there, from command line tools to libraries for programming languages. Because the tar file format leaves room for interpretation, different implementations can extract certain crafted tar files in different ways.

This is a security concern: for example, when a security scanner and the extractor use different tar implementations, the scanner could inspect other files than the ones that end up on disk.

By assigning [identifiers](https://stoppels.ch/tar/#policy) to these ambiguities, and providing test cases and usage data, the hope is that tar implementations can converge on a strict parser and identical behavior.

This project proposes a **[default policy](https://stoppels.ch/tar/#policy)** that rejects the vast majority of ambiguities in tar files that could make implementations extract different files, while ensuring that nearly every source tarball already published can still be extracted. <!-- begin strict.py -->Of the 82,587 source tarballs of Spack, nixpkgs, Guix, live-bootstrap, PyPI, crates.io and RubyGems, it accepts 99.79% ([per ecosystem](https://stoppels.ch/tar/#tarballs)).<!-- end strict.py -->

## Motivating examples

| case | the archive | what implementations make of it |
|---|---|---|
| [N09](https://stoppels.ch/tar/N09.html) | two pax headers for one file, with `path=first` and `path=second` | GNU tar, node-tar and Go extract `second`; Python and Java extract `first`; bsdtar, Rust and .NET reject it |
| [S10](https://stoppels.ch/tar/S10.html) | a symlink `a` to `target`, then a file `a` | most replace the link with the file; Python's tarfile writes through the link, to `target` |
| [K01](https://stoppels.ch/tar/K01.html) | a regular file named `a/` | GNU tar, bsdtar, node-tar and Java create a directory `a`; Python, Go, Rust's `tar` and PHP's PharData an empty file `a`; tar-fs and .NET reject it |
| [F12](https://stoppels.ch/tar/F12.html) | a size field of `000000 1000`, with a space | GNU tar, node-tar and tar-fs read 0, and find a second file `smuggled` in the data; bsdtar, Python, Go, Rust, Java and .NET reject it |

Use **[the test suite](suite/)** in your tests, or browse **[the website](https://stoppels.ch/tar/)** for what each case means, what implementations make of it, and how often it occurs in source tarballs.

## Comparison

<!-- begin matrix.py -->
What 26 implementations make of the 72 cases: a row per case, by category, and a column per implementation, with the outcomes of all cases at the top. [The website](https://stoppels.ch/tar/) has a page per case.

[![What every implementation makes of every case of the test suite. Outcomes of all cases: strict.py: ✅72; GNU tar: ✅34 ⚠️38; bsdtar: ✅33 ⚠️39; BusyBox tar: ✅26 ⚠️45 ❌1; 7-Zip: ✅27 ⚠️43 ⛔1 ❌1; Python tarfile, filter=data, as in pip: ✅33 ⚠️38 ⛔1; Python tarfile, filter=tar: ✅33 ⚠️39; Python tarfile, filter=fully_trusted: ✅32 ⚠️38 💥2; node-tar: ✅23 ⚠️48 ❌1; node-tar, strict: ✅33 ⚠️38 ⛔1; tar-fs: ✅35 ⚠️35 ⛔2; Java Commons Compress: ✅32 ⚠️39 ❌1; .NET System.Formats.Tar: ✅49 ⚠️21 ⛔2; PHP PharData, as in Composer: ✅24 ⚠️43 ⛔1 ❌4; Go archive/tar: ✅31 ⚠️41; Go archive/tar, tarinsecurepath=0: ✅34 ⚠️38; Go containerd archive.Apply: ✅34 ⚠️38; Rust tar: ✅31 ⚠️41; Rust astral-tokio-tar: ✅38 ⚠️33 ⛔1; Rust tar-codec, as in uv: ✅55 ⚠️11 ⛔4 ❌2; RubyGems: ✅23 ⚠️42 ⛔2 ❌5; R untar, internal: ✅37 ⚠️35; Perl Archive::Tar: ✅29 ⚠️40 ⛔1 ❌2; Haskell tar: ✅33 ⚠️33 ⛔5 ❌1; Julia Tar.jl: ✅44 ⚠️28; live-bootstrap untar: ✅19 ⚠️43 ❌8 💥2; live-bootstrap untar, --non-strict: ✅14 ⚠️48 ❌8 💥2](contrib/matrix/matrix.svg)](https://stoppels.ch/tar/)
<!-- end matrix.py -->

## Contents

- [suite/](suite): the test suite. Copy it into your tests; its README describes the format.
- [METHOD.md](METHOD.md): the terms, the catalogue of ambiguities, the verdicts and the default policy.
- [contrib/](contrib): how the data was made.
- [docs/](docs): the website.

## Contributing

Issues and pull requests are welcome on [GitHub](https://github.com/haampie/tar-minefield/issues): a new case, an implementation for the comparison, or a tarball that the default policy gets wrong.

Contributors:

- [Harmen Stoppels](https://github.com/haampie)
- [William Woodruff](https://github.com/woodruffw)

# Tar file extraction test suite

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23617964.svg)](https://doi.org/10.5281/zenodo.23617964)

This project provides an extensive **[test suite](suite/)** and **[documentation](https://stoppels.ch/tar/)** for tar file extraction, with the goal of ensuring that implementations extract tar archives the same way.

There are many implementations of tar, from command line tools to libraries for programming languages. Because the tar file format leaves room for interpretation, different implementations can extract [certain crafted tar files](#motivating-examples) in different ways.

This is a security concern for file exchange: for example, when a security scanner and the extractor use different tar implementations, the scanner could inspect other files than the ones that end up on disk.

By assigning [identifiers](https://stoppels.ch/tar/#policy) to these ambiguities, and providing test cases and usage data, this project aims for tar implementations to converge on strict parsing and identical behavior.

This project proposes a **[default policy](https://stoppels.ch/tar/#policy)** that rejects the vast majority of ambiguities in tar files that could make implementations extract different files, while ensuring that nearly every source tarball already published can still be extracted. <!-- begin strict.py -->Of the 82,586 source tarballs of Spack, nixpkgs, Guix and live-bootstrap, and samples of PyPI, crates.io and RubyGems, it accepts 99.77% ([per ecosystem](https://stoppels.ch/tar/#tarballs)).<!-- end strict.py -->

## Motivating examples

| case | the archive | what implementations make of it |
|---|---|---|
| [N09](https://stoppels.ch/tar/N09.html) | two pax headers for one file, with `path=first` and `path=second` | GNU tar, BusyBox, 7-Zip, node-tar, tar-fs, Go, R and Julia extract `second`; Python and Java extract `first`; PHP, RubyGems, Perl and live-bootstrap extract `header-name`, the name in the ustar header; bsdtar, Rust, .NET and Haskell reject it |
| [S10](https://stoppels.ch/tar/S10.html) | a symlink `a` to `target`, then a file `a` | most replace the link with the file; Python's `tarfile` and live-bootstrap write through the link, to `target`; 7-Zip, .NET and Haskell reject it |
| [K01](https://stoppels.ch/tar/K01.html) | a regular file named `a/` | GNU tar, bsdtar, BusyBox, 7-Zip, node-tar, Java, Perl and live-bootstrap create a directory `a`; Python, Go, Rust's `tar` and astral-tokio-tar, PHP's `PharData`, RubyGems and R an empty file `a`; tar-fs, .NET, Haskell, Julia and tar-codec reject it |
| [F12](https://stoppels.ch/tar/F12.html) | a size field of `000000 1000`, with a space | GNU tar, BusyBox, 7-Zip, node-tar, tar-fs, Perl, Haskell, Julia and live-bootstrap read 0, and find a second file `smuggled` in the data; R reads 512, and extracts it as the data of `a`; bsdtar, Python, Go, Rust, Java, .NET, PHP and RubyGems reject it |

Use **[the test suite](suite/)** in your tests, or browse **[the website](https://stoppels.ch/tar/)** for what each case means, what implementations make of it, and how often it occurs in release tarballs.

## Comparison

<!-- begin matrix.py -->
What 20 implementations make of the 74 cases: a row per case, by category, and a column per implementation, with the outcomes of all cases at the top. [The website](https://stoppels.ch/tar/) has a page per case.

[![What every implementation makes of every case of the test suite. Outcomes of all cases: GNU tar: ✅23 ➕10 ⚠️41; bsdtar: ✅24 ➕10 ⚠️40; BusyBox tar: ✅15 ➕9 ⚠️49 ❌1; 7-Zip: ✅19 ➕9 ⚠️45 ❌1; Python tarfile, filter=data, as in pip: ✅23 ➕9 ➖1 ⚠️41; Python tarfile, filter=tar: ✅22 ➕10 ⚠️42; Python tarfile, filter=fully_trusted: ✅20 ➕10 ⚠️41 💥3; node-tar: ✅13 ➕9 ⚠️51 ❌1; node-tar, strict: ✅23 ➕9 ➖1 ⚠️41; tar-fs: ✅26 ➕8 ➖2 ⚠️38; Java Commons Compress: ✅22 ➕9 ⚠️42 ❌1; .NET System.Formats.Tar: ✅42 ➕8 ➖2 ⚠️22; PHP PharData, as in Composer: ✅17 ➕7 ➖1 ⚠️46 ❌3; Go containerd archive.Apply: ✅23 ➕10 ⚠️41; Rust tar: ✅20 ➕10 ⚠️44; Rust astral-tokio-tar: ✅28 ➕9 ➖1 ⚠️36; Rust tar-codec, as in uv: ✅51 ➕5 ➖5 ⚠️13; RubyGems: ✅18 ➕7 ➖2 ⚠️44 ❌3; R untar, internal: ✅26 ➕10 ⚠️38; Perl Archive::Tar: ✅17 ➕8 ➖1 ⚠️46 ❌2; Haskell tar: ✅30 ➕6 ➖3 ⚠️34 ❌1; Julia Tar.jl: ✅35 ➕10 ⚠️29; live-bootstrap untar: ✅17 ➕8 ⚠️38 ❌8 💥3; live-bootstrap untar, --non-strict: ✅10 ➕8 ⚠️45 ❌8 💥3](contrib/matrix/matrix.svg)](https://stoppels.ch/tar/)
<!-- end matrix.py -->

## Contents

- [suite/](suite): the test suite. Copy it into your tests; its README describes the format.
- [METHOD.md](METHOD.md): the terms, the catalogue of ambiguities, the verdicts and the default policy.
- [contrib/](contrib): how the data was made.
- [docs/](docs): the website.

## Contributing

Issues and pull requests are welcome on [GitHub](https://github.com/haampie/tar-minefield/issues): a new case, an implementation for the comparison, or a tarball that the default policy gets wrong. A case that shows a vulnerability that is not yet disclosed is reported privately first: see [SECURITY.md](SECURITY.md).

Contributors:

- [Harmen Stoppels](https://github.com/haampie)
- [William Woodruff](https://github.com/woodruffw)

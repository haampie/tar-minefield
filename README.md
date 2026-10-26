# Tar file extraction test suite

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23617964.svg)](https://doi.org/10.5281/zenodo.23617964)

This project provides an extensive **[test suite](suite/)** and **[documentation](https://stoppels.ch/tar/)** for tar file extraction, with the goal of ensuring that implementations extract tar archives the same way.

There are many implementations of tar, from command line tools to libraries for programming languages. Because the tar file format leaves room for interpretation, different implementations can extract [certain crafted tar files](#motivating-examples) in different ways.

This is a security concern for file exchange: for example, when a security scanner and the extractor use different tar implementations, the scanner could inspect other files than the ones that end up on disk.

By assigning [identifiers](https://stoppels.ch/tar/#policy) to these ambiguities, and providing test cases and usage data, this project aims for tar implementations to converge on strict parsing and identical behavior.

This project proposes a **[default policy](https://stoppels.ch/tar/#policy)** that rejects the vast majority of ambiguities in tar files that could make implementations extract different files, while ensuring that nearly every source tarball already published can still be extracted. <!-- begin strict.py -->Of the 82,586 source tarballs of Spack, nixpkgs, Guix and live-bootstrap, and samples of PyPI, crates.io and RubyGems, it [accepts 99.77%](https://stoppels.ch/tar/#tarballs).<!-- end strict.py -->

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
What 20 implementations make of the 78 cases: a row per case, by category, and a column per implementation, with the outcomes of all cases at the top. [The website](https://stoppels.ch/tar/) has a page per case.

[![What every implementation makes of every case of the test suite. Outcomes of all cases: GNU tar: ✅26 ➕10 ⚠️42; bsdtar: ✅28 ➕10 ⚠️40; BusyBox tar: ✅15 ➕9 ⚠️53 ❌1; 7-Zip: ✅19 ➕9 ⚠️49 ❌1; Python tarfile, filter=data, as in pip: ✅25 ➕9 ➖1 ⚠️43; Python tarfile, filter=tar: ✅24 ➕10 ⚠️44; Python tarfile, filter=fully_trusted: ✅22 ➕10 ⚠️43 💥3; node-tar: ✅14 ➕9 ⚠️54 ❌1; node-tar, strict: ✅25 ➕9 ➖1 ⚠️43; tar-fs: ✅26 ➕8 ➖2 ⚠️42; Java Commons Compress: ✅23 ➕9 ⚠️45 ❌1; .NET System.Formats.Tar: ✅45 ➕8 ➖2 ⚠️23; PHP PharData, as in Composer: ✅18 ➕7 ➖1 ⚠️49 ❌3; Go containerd archive.Apply: ✅26 ➕10 ⚠️42; Rust tar: ✅22 ➕10 ⚠️46; Rust astral-tokio-tar: ✅31 ➕9 ➖1 ⚠️37; Rust tar-codec, as in uv: ✅55 ➕5 ➖5 ⚠️13; RubyGems: ✅19 ➕7 ➖2 ⚠️47 ❌3; R untar, internal: ✅17 ➕10 ⚠️51; Perl Archive::Tar: ✅19 ➕8 ➖1 ⚠️48 ❌2; Haskell tar: ✅32 ➕6 ➖3 ⚠️36 ❌1; Julia Tar.jl: ✅38 ➕10 ⚠️30; live-bootstrap untar: ✅19 ➕8 ⚠️40 ❌8 💥3; live-bootstrap untar, --non-strict: ✅10 ➕8 ⚠️49 ❌8 💥3](contrib/matrix/matrix.svg)](https://stoppels.ch/tar/)
<!-- end matrix.py -->

## Contents

- [suite/](suite): the test suite. Copy it into your tests; its README describes the format.
- [METHOD.md](METHOD.md): the terms, the catalogue of ambiguities, the verdicts and the default policy.
- [contrib/](contrib): how the data was made.
- [docs/](docs): the website.

## Contributing

This project is looking for contributions from people who work on package managers, registries and tar implementations, in the form of discussions in [issues or pull requests on GitHub](https://github.com/haampie/tar-minefield/issues) or by email to harmen at stoppels dot ch, so that the working draft of the default policy can become a reference.

You can also contribute by testing other implementations, or by crafting a tarball that is particularly hard to parse. A case that shows a vulnerability that is not yet disclosed is reported privately first: see [SECURITY.md](SECURITY.md).

Contributors:

- [Harmen Stoppels](https://github.com/haampie)
- [William Woodruff](https://github.com/woodruffw)

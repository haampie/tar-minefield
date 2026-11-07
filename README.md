# Tar file extraction test suite

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23617964.svg)](https://doi.org/10.5281/zenodo.23617964)

This project provides an extensive **[test suite](suite/)** and **[documentation](https://stoppels.ch/tar/)** for tar file extraction, with the goal of ensuring that implementations extract tar archives the same way.

There are many implementations of tar, from command line tools to libraries for programming languages. Because the tar file format leaves room for interpretation, different implementations can extract [certain crafted tar files](#motivating-examples) in different ways.

This is a security concern for file exchange: for example, when a security scanner and the extractor use different tar implementations, the scanner could inspect other files than the ones that end up on disk.

By assigning [identifiers](https://stoppels.ch/tar/#policy) to these ambiguities, and providing test cases and usage data, this project aims for tar implementations to converge on strict parsing and identical behavior.

This project proposes a **[default policy](https://stoppels.ch/tar/#policy)** that rejects the vast majority of ambiguities in tar files that could make implementations extract different files, while ensuring that nearly every source tarball already published can still be extracted. <!-- begin strict.py -->Of the 82,586 source tarballs of Spack, nixpkgs, Guix and live-bootstrap, and samples of PyPI, crates.io and RubyGems, it [accepts 99.80%](https://stoppels.ch/tar/#tarballs).<!-- end strict.py -->

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
What 20 implementations make of the 134 cases: a row per case, by category, and a column per implementation, with the outcomes of all cases at the top. [The website](https://stoppels.ch/tar/) has a page per case.

[![What every implementation makes of every case of the test suite. Outcomes of all cases: GNU tar: ✅50 ➕17 ⚠️67; bsdtar: ✅51 ➕17 ⚠️66; BusyBox tar: ✅37 ➕16 ⚠️80 ❌1; 7-Zip: ✅35 ➕14 ➖2 ⚠️81 ❌2; Python tarfile, filter=data, as in pip: ✅46 ➕15 ➖2 ⚠️71; Python tarfile, filter=tar: ✅42 ➕17 ⚠️75; Python tarfile, filter=fully_trusted: ✅39 ➕17 ⚠️75 💥3; node-tar: ✅24 ➕15 ⚠️90 ❌5; node-tar, strict: ✅40 ➕15 ➖2 ⚠️74 ❌3; tar-fs: ✅52 ➕13 ➖4 ⚠️65; Java Commons Compress: ✅41 ➕14 ⚠️72 ❌7; .NET System.Formats.Tar: ✅76 ➕14 ➖3 ⚠️38 ❌3; PHP PharData, as in Composer: ✅31 ➕11 ➖3 ⚠️77 ❌12; Go containerd archive.Apply: ✅48 ➕16 ➖1 ⚠️69; Rust tar: ✅43 ➕17 ⚠️73 ❌1; Rust astral-tokio-tar: ✅58 ➕16 ➖1 ⚠️59; Rust tar-codec, as in uv: ✅107 ➕7 ➖10 ⚠️10; RubyGems: ✅29 ➕10 ➖4 ⚠️77 ❌14; R untar, internal: ✅31 ➕15 ➖2 ⚠️77 ❌9; Perl Archive::Tar: ✅31 ➕13 ➖2 ⚠️77 ❌11; Haskell tar: ✅55 ➕11 ➖5 ⚠️60 ❌3; Julia Tar.jl: ✅72 ➕16 ➖1 ⚠️45; live-bootstrap untar: ✅31 ➕10 ➖3 ⚠️64 ❌23 💥3; live-bootstrap untar, --non-strict: ✅16 ➕10 ➖2 ⚠️79 ❌24 💥3](contrib/matrix/matrix.svg)](https://stoppels.ch/tar/)
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

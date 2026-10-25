# Scan of all 19086 nixpkgs tarballs

- tarballs: 19086, scanned: 19012 (17977 latest versions, 1035 older)
- not downloaded: 74, scanner crashed: 0
- downloaded from the first of their URLs (a mirror): 9377
- copied from other scans with `--reuse`: 11, read from `--cache`: 0; sources by host: tarballs.nixos.org 9377, hackage.haskell.org 6139, files.pythonhosted.org 1452, download.kde.org 466, code.call-cc.org 336, download.gnome.org 256
- size: 78.3 GB compressed
- origins: other 11975, pypi 3846, cpan 1899, github-release 813, gnu 308, cran/bioconductor 81, github-archive 50, gitlab 28, crates.io 12
- producers: ustar 10207, GNU format 4268, Python tarfile (pax) 3087, v7 771, git archive 394, GNU tar (pax) 224, libarchive (pax) 30, none 22, posix-version-0000 9
- compression: gzip 16300, xz 1555, bzip2 830, none 327
- scanner stopped early: 22
  - ocrad@0.29: invalid checksum at offset 0
  - git-warp-time@1.0.0: invalid checksum at offset 0
  - wget@1.25.0: invalid checksum at offset 0
  - ddrescue@1.30: invalid checksum at offset 0
  - Libertinus@7.051: invalid checksum at offset 0
  - fcitx5-rime@5.1.16: invalid checksum at offset 0
  - decasify@0.11.4: invalid checksum at offset 0
  - ed@1.22.6: invalid checksum at offset 0
  - rcs@5.10.1: invalid checksum at offset 0
  - moe@1.16: invalid checksum at offset 0
  - maptool@1.18.7-x86_64.pkg: invalid checksum at offset 0
  - bc@1.08.2: invalid checksum at offset 0
  - plzip@1.13: invalid checksum at offset 0
  - goredo@2.10.0: invalid checksum at offset 0
  - libpsl@0.21.5: invalid checksum at offset 0
  - fcitx5-anthy@5.1.11: invalid checksum at offset 0
  - parsers-linux-x86_64@: invalid checksum at offset 0
  - lzlib@1.16: invalid checksum at offset 0
  - vors@6.3.0: invalid checksum at offset 0
  - sile@0.15.13: invalid checksum at offset 0
  - warp-terminal@v0.2026.10.14.08.27.stable_01-1-x86_64.pkg: invalid checksum at offset 0
  - tarlz@0.30: invalid checksum at offset 0

## untar

Rejects 100 of 19012 (0.5%); 94 of 17977 latest versions (0.5%).

| reason | tarballs | latest | origins | producers | examples |
|---|---:|---:|---|---|---|
| FileExistsError: [Errno N] File exists: '…' | 59 | 54 | other 57, pypi 1, github-release 1 | ustar 50, git archive 4, Python tarfile (pax) 4 | snap-loader-static@1.0.0.1; htn@0.1.0.0; shelly-extra@0.3.0.2 |
| Archive contains an invalid number b'…' | 22 | 22 | gnu 10, github-release 7, other 5 | none 22 | ocrad@0.29; git-warp-time@1.0.0; wget@1.25.0 |
| Archive is truncated | 9 | 8 | other 9 | ustar 4, GNU format 4, v7 1 | SDL2_ttf@2.24.0; SDL2_image@2.8.12; eng-rus@ |
| Archive contains data after the end-of-archive marker | 8 | 8 | other 6, cpan 1, github-release 1 | v7 4, posix-version-0000 2, ustar 2 | bsf-bin@2.4.0; psutils-p17@; Logfile-Rotate@1.04 |
| Archive contains unsafe path … | 1 | 1 | other 1 | git archive 1 | dtv-scan-tables@2024-03-24-7098bdd27548 |
| Archive contains forktty-N.N/pipe of unsupported type b'…' | 1 | 1 | other 1 | GNU format 1 | forktty@1.3 |

## Features

Number of tarballs with each feature, of which latest versions; their origins, producers and median mtime years, and what untar did with them.

| feature | tarballs | latest | origins | producers | years | untar rejects | examples |
|---|---:|---:|---|---|---|---:|---|
| `name.dir-without-trailing-slash` | 817 | 765 | cpan 431, github-release 293, other 78 | ustar 784, GNU format 26, GNU tar (pax) 7 | 1970–2026 | 0 | Catalyst-DispatchType-Regex@5.90035 `Catalyst-DispatchType-Regex-5.90035`; Boost-Geometry-Utils@0.15 `Boost-Geometry-Utils-0.15` |
| `name.fills-field` | 806 | 723 | other 368, pypi 351, github-release 64 | GNU format 311, Python tarfile (pax) 298, ustar 124 | 1970–2026 | 7 | google_cloud_workflows@1.24.0 `google_cloud_workflows-1.24.0/google/cloud/workflows/executi`; aliyun-python-sdk-drds@20210523.0.2 `aliyun-python-sdk-drds-20210523.0.2/aliyunsdkdrds/request/v2` |
| `type.nul` | 774 | 744 | other 598, gnu 115, github-release 42 | v7 761, GNU format 13 | 1970–2026 | 4 | grep@3.12 `grep-3.12/.mailmap`; autoconf@2.69 `autoconf-2.69/THANKS` |
| `tree.dir-after-contents` | 747 | 709 | other 712, cpan 20, pypi 15 | ustar 724, GNU format 17, posix-version-0000 4 | 1970–2026 | 7 | streaming-utils@0.2.6.0 `streaming-utils-0.2.6.0/Streaming/`; distributed-closure@0.5.0.0 `distributed-closure-0.5.0.0/src/Data/Profunctor/` |
| `ustar.prefix` | 621 | 574 | cpan 334, other 215, github-release 49 | ustar 549, git archive 65, libarchive (pax) 4 | 1981–2026 | 7 | Boost-Geometry-Utils@0.15 `Build.PL`; LWP-Protocol-https@6.11 `Changes` |
| `number.chksum.leading-space` | 546 | 543 | cpan 490, other 50, github-release 4 | ustar 486, GNU format 33, v7 17 | 1992–2026 | 12 | Catalyst-DispatchType-Regex@5.90035; Boost-Geometry-Utils@0.15 |
| `v7.bytes-after-linkname` | 546 | 520 | other 436, gnu 83, github-release 22 | v7 546 | 1970–2026 | 0 | autoconf@2.69 `autoconf-2.69/`; pkg-config@0.29.2 `pkg-config-0.29.2/` |
| `number.size.leading-space` | 545 | 542 | cpan 490, other 50, github-release 3 | ustar 486, GNU format 33, v7 17 | 1992–2026 | 11 | Catalyst-DispatchType-Regex@5.90035 `Catalyst-DispatchType-Regex-5.90035`; Boost-Geometry-Utils@0.15 `Boost-Geometry-Utils-0.15` |
| `name.non-ascii` | 74 | 56 | other 56, pypi 6, github-release 5 | GNU format 48, Python tarfile (pax) 10, GNU tar (pax) 6 | 2004–2026 | 0 | aisleriot@3.22.35 `aisleriot-3.22.35/cards/README.Атласные`; node@v26.12.1 `node-v26.12.1/test/fixtures/copy/utf/新建文件夹/` |
| `platform.case-collision` | 66 | 52 | other 53, gnu 6, github-archive 3 | git archive 20, GNU format 17, ustar 12 | 1980–2026 | 1 | onboard@1.4.1 `onboard-1.4.1/onboard`; public-inbox@2.1.0 `public-inbox-2.1.0/install/` |
| `number.gid.no-digits` | 65 | 58 | pypi 36, other 13, crates.io 12 | GNU format 38, ustar 22, posix-version-0000 5 | 1970–2026 | 0 | hadoop@3.4.2-src `hadoop-3.4.2-src/README.txt`; ipv8_rust_tunnels@0.1.53 `ipv8_rust_tunnels-0.1.53/PKG-INFO` |
| `number.uid.no-digits` | 65 | 58 | pypi 36, other 13, crates.io 12 | GNU format 38, ustar 22, posix-version-0000 5 | 1970–2026 | 0 | hadoop@3.4.2-src `hadoop-3.4.2-src/README.txt`; ipv8_rust_tunnels@0.1.53 `ipv8_rust_tunnels-0.1.53/PKG-INFO` |
| `number.gid.leading-space` | 62 | 59 | other 50, cpan 9, gnu 2 | GNU format 33, v7 17, posix-version-0000 8 | 1992–2026 | 11 | hadoop@3.4.2-src `hadoop-3.4.2-src/`; nld-eng@ `nld-eng.dict.dz` |
| `number.uid.leading-space` | 62 | 59 | other 50, cpan 9, gnu 2 | GNU format 33, v7 17, posix-version-0000 8 | 1992–2026 | 11 | hadoop@3.4.2-src `hadoop-3.4.2-src/`; nld-eng@ `nld-eng.dict.dz` |
| `tree.duplicate.file-file` | 59 | 54 | other 57, pypi 1, github-release 1 | ustar 50, git archive 4, Python tarfile (pax) 4 | 1970–2026 | 59 | snap-loader-static@1.0.0.1 `snap-loader-static-1.0.0.1/LICENSE`; htn@0.1.0.0 `htn-0.1.0.0/src/Algorithms/Htn.hs` |
| `number.mode.leading-space` | 55 | 52 | other 43, cpan 9, gnu 2 | GNU format 28, v7 16, posix-version-0000 8 | 1992–2026 | 8 | hadoop@3.4.2-src `hadoop-3.4.2-src/`; uuid@1.6.2 `uuid-1.6.2/AUTHORS` |
| `number.mtime.leading-space` | 39 | 39 | other 30, cpan 8, gnu 1 | GNU format 28, v7 8, ustar 3 | 1992–2004 | 8 | nld-eng@ `nld-eng.dict.dz`; bsd-finger_0.17.orig@ `bsd-finger-0.17/` |
| `name.leading-dot-slash` | 35 | 33 | other 20, github-release 13, gnu 1 | GNU format 29, ustar 3, GNU tar (pax) 1 | 1998–2026 | 1 | curie@v1.0 `./LICENSE`; hdf5@1.10.11 `./hdf5-1.10.11/` |
| `number.uid.base256` | 34 | 33 | pypi 14, cpan 12, other 7 | GNU format 30, libarchive (pax) 4 | 2008–2026 | 0 | leo@2_v1.7.0 `leo2/`; Bytes-Random-Secure-Tiny@1.011 `Bytes-Random-Secure-Tiny-1.011/` |
| `number.gid.base256` | 29 | 28 | pypi 13, cpan 11, other 4 | GNU format 26, libarchive (pax) 3 | 2008–2026 | 0 | Bytes-Random-Secure-Tiny@1.011 `Bytes-Random-Secure-Tiny-1.011/`; pyannotate@1.2.0 `pyannotate-1.2.0/` |
| `platform.windows-invalid-character` | 28 | 27 | other 22, pypi 2, gnu 2 | GNU format 12, git archive 6, Python tarfile (pax) 5 | 2003–2026 | 1 | xitomatl_0.0.0-akku.208.62a8243_repack@ `fmt/let-optionals*.larceny.sls`; courier-unicode@2.6.0 `courier-unicode-2.6.0/man/unicode::ucs_4.3` |
| `name.dot` | 18 | 16 | github-release 12, other 5, cpan 1 | GNU format 17, v7 1 | 1998–2026 | 1 | partclone-utils@0.4.3 `./`; cmucl@21d-x86-linux `./` |
| `pax.nul-in-value.SCHILY.xattr.*` | 16 | 16 | cpan 10, other 5, github-release 1 | libarchive (pax) 16 | 2019–2026 | 0 | Crypt-X509@0.55 `Crypt-X509-0.55/PaxHeader/README`; djview@4.12.3 `PaxHeader/djview-4.12.3` |
| `pax.value-not-utf8.SCHILY.xattr.*` | 16 | 16 | cpan 10, other 5, github-release 1 | libarchive (pax) 16 | 2019–2026 | 0 | Crypt-X509@0.55 `Crypt-X509-0.55/PaxHeader/README`; djview@4.12.3 `PaxHeader/djview-4.12.3` |
| `platform.windows-reserved-name` | 16 | 10 | other 13, gnu 1, github-release 1 | git archive 8, GNU format 5, v7 2 | 2010–2026 | 0 | linux@6.12.91 `linux-6.12.91/drivers/gpu/drm/nouveau/nvkm/subdev/i2c/aux.c`; mvapich@4.1 `mvapich-4.1/modules/ucx/config/aux/` |
| `linkname.no-nul` | 15 | 5 | other 14, github-release 1 | GNU format 13, Python tarfile (pax) 2 | 2023–2026 | 0 | ghc@9.12.4-src `ghc-9.12.4/libraries/Cabal/cabal-testsuite/PackageTests/Requ`; nextcloud@34.0.5 `nextcloud/apps/app_api/js/app_api-vendors-node_modules_nextc` |
| `symlink.absolute` | 15 | 15 | other 14, github-release 1 | GNU format 9, ustar 2, git archive 2 | 2008–2026 | 1 | live.2026.01.12@ `live/testProgs/whiteroom.mp3`; imapsync@2.314 `imapsync-2.314/X/fullchain.pem` |
| `tree.duplicate.dir-dir` | 11 | 11 | other 8, github-release 3 | git archive 8, ustar 3 | 2021–2026 | 2 | besu@24.1.2 `besu-24.1.2/./`; lightweight-testing@0.1 `lightweight-testing-0.1/./` |
| `magic.posix-version-nuls` | 9 | 7 | other 7, github-release 2 | posix-version-0000 9 | 2006–2026 | 2 | hadoop@3.4.2-src `hadoop-3.4.2-src/README.txt`; bsf-bin@2.4.0 `bsf-2.4.0/` |
| `number.gid.no-terminator` | 9 | 9 | cpan 9 | ustar 9 | 2014–2022 | 0 | App-rainbarf@1.4 `App-rainbarf-1.4`; JSON-WebToken@0.10 `Build.PL` |
| `number.uid.no-terminator` | 9 | 9 | cpan 9 | ustar 9 | 2014–2022 | 0 | App-rainbarf@1.4 `App-rainbarf-1.4`; JSON-WebToken@0.10 `Build.PL` |
| `platform.windows-trailing-dot-or-space` | 9 | 8 | other 8, gnu 1 | Python tarfile (pax) 2, git archive 2, v7 2 | 2000–2026 | 0 | knot-resolver@5.7.9 `knot-resolver-5.7.9/tests/integration/deckard/sets/resolver/`; knot-resolver@6.5.1 `knot-resolver-6.5.1/tests/integration/deckard/sets/resolver/` |
| `end.data-after` | 8 | 8 | other 6, cpan 1, github-release 1 | v7 4, posix-version-0000 2, ustar 2 | 1995–2012 | 8 | bsf-bin@2.4.0 `bsf-2.4.0/samples/xsl/table-data.xml`; psutils-p17@ `psutils/showchar.sh` |
| `pax-global.after-members` | 7 | 7 | other 5, github-release 2 | git archive 7 | 2022–2026 | 1 | inform@6.44-r3 `pax_global_header`; rpm@4.20.1 `pax_global_header` |
| `pax.newline-in-value.SCHILY.xattr.*` | 7 | 7 | cpan 5, other 2 | libarchive (pax) 7 | 2020–2025 | 0 | Minion@10.31 `Minion-10.31/lib/Mojolicious/Plugin/Minion/resources/public/`; Term-ReadLine-Gnu@1.47 `Term-ReadLine-Gnu-1.47/t/comptest/PaxHeader/README` |
| `end.lone-zero-block` | 5 | 5 | other 5 | GNU format 4, v7 1 | 1998–2014 | 5 | eng-rus@ `eng-rus.index`; srecord@1.64 `srecord-1.64/debian/srecord.install` |
| `name.dot-component` | 5 | 4 | other 5 | ustar 3, GNU format 1, GNU tar (pax) 1 | 2018–2026 | 0 | besu@24.1.2 `besu-24.1.2/./`; lightweight-testing@0.1 `lightweight-testing-0.1/./` |
| `end.missing` | 4 | 3 | other 4 | ustar 4 | 2023–2026 | 4 | SDL2_ttf@2.24.0 `SDL2_ttf-2.24.0/external/harfbuzz/README`; SDL2_image@2.8.12 `SDL2_image-2.8.12/Xcode/macOS/SDL2.framework/Resources` |
| `name.trailing-slash-on-file` | 4 | 4 | other 4 | v7 4 | 1994–2023 | 2 | sendmail.8.18.2@ `sendmail-8.18.2/`; tcp_wrappers_7.6@ `tcp_wrappers_7.6/` |
| `tree.under-file` | 3 | 3 | other 3 | v7 3 | 1994–2023 | 1 | sendmail.8.18.2@ `sendmail-8.18.2/Makefile`; tcp_wrappers_7.6@ `tcp_wrappers_7.6/README` |
| `name.not-utf8` | 2 | 2 | gnu 2 | GNU format 2 | 2004–2004 | 0 | aspell-is@0.51.1-0 `aspell-is-0.51.1-0/\xedslenska.alias`; aspell-nb@0.50.1-0 `aspell-nb-0.50.1-0/bokm\xe5l.alias` |
| `number.mtime.no-digits` | 2 | 2 | github-release 2 | ustar 2 | 2025–2026 | 0 | camunda-modeler@5.52.0-linux-x64 `camunda-modeler-5.52.0-linux-x64/`; stretchly@1.19.0 `Stretchly-1.19.0/` |
| `pax.LIBARCHIVE.creationtime` | 2 | 2 | other 1, cpan 1 | libarchive (pax) 2 | 2015–2015 | 0 | leo@2_v1.7.0 `leo2/`; Proc-Wait3@0.05 `Proc-Wait3-0.05/Changes` |
| `hardlink.to-itself` | 1 | 1 | other 1 | GNU format 1 | 2020–2020 | 0 | atari++_1.85@ `atari++/winmain.cpp` |
| `name.absolute` | 1 | 1 | other 1 | git archive 1 | 2024–2024 | 1 | dtv-scan-tables@2024-03-24-7098bdd27548 `/usr/share/dvb/` |
| `name.backslash` | 1 | 1 | gnu 1 | ustar 1 | 2010–2010 | 0 | texi2html@5.0 `texi2html-5.0/test/info_coverage/f--ile""\.png` |
| `name.control-character` | 1 | 1 | other 1 | ustar 1 | 2009–2009 | 0 | cdrtools@3.02a09 `cdrtools-3.02/libfind/if\x1bpdi` |
| `name.double-slash` | 1 | 0 | other 1 | GNU format 1 | 2021–2021 | 0 | ghc@9.0.2-x86_64-deb10-linux `ghc-9.0.2/libraries/ghc-bignum/dist-install/build/include//H` |
| `pax.size-on-dir` | 1 | 1 | pypi 1 | GNU tar (pax) 1 | 1970–1970 | 0 | llama_index_workflows@2.26.0 `llama_index_workflows-2.26.0/` |
| `tree.duplicate.file-hardlink` | 1 | 1 | other 1 | GNU format 1 | 2020–2020 | 0 | atari++_1.85@ `atari++/winmain.cpp` |

## Fingerprints

- magic (tarballs using each): posix 13942, gnu 4285, v7 771, posix-version-0000 9
- size (tarballs using each): dn 17601, ds 834, sdn 489, sds 56, dsn 11
- mode (tarballs using each): dn 18082, dsn 822, ds 67, sdsn 48, sdn 7
- checksum (tarballs using each): dns 17040, dn 1060, sdns 528, d 339, dsn 15, x 15, sdsn 9, ds 8, sdn 5, sds 3, xd 2, xdx 2
- pax_header_name (tarballs using each): ././@PaxHeader 3088, */PaxHeaders/* 172, ./PaxHeaders/* 144, */PaxHeaders.N/* 36, ./PaxHeaders.N/* 34, */PaxHeader/* 29, ./PaxHeaders.X/* 16, PaxHeader/* 13, */PaxHeaders 9, ./PaxHeaders.X/eclipse_plugins_org.eclipse.platform_N.N.N.vN-N_eclipse_lg@Nx.png 8, H.paxheader 7, * 7
- extended_sequence (tarballs using each): - 15866, x 3352, L 475, KL 9, K 8
- gnu_long_name (tarballs using each): ././@LongLink 475
- end (tarballs using each): padded-to-10240 10509, unpadded 8472
- zero_blocks_after_end (tarballs using each): 0 9427, 11 558, 9 535, 6 523, 16 517, 1 516, 17 508, 8 508, 10 507, 4 505, 2 502, 19 498
- pax_keys (tarballs using each): mtime 3275, path 609, atime 135, ctime 129, uid 30, gid 28, LIBARCHIVE.xattr.* 20, SCHILY.xattr.* 19, SCHILY.dev 5, SCHILY.ino 5, SCHILY.nlink 5, LIBARCHIVE.creationtime 2
- pax_global_keys (tarballs using each): comment 394
- compression layer: trailing zeros 1, several streams 1

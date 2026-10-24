# Scan of a sample of 5000 gems

- tarballs: 5000, scanned: 5000 (2500 latest versions, 2500 older)
- not downloaded: 0, scanner crashed: 0
- downloaded from the first of their URLs (a mirror): 5000
- copied from other scans with `--reuse`: 0, read from `--cache`: 0; sources by host: rubygems.org 5000
- size: 1.0 GB compressed
- origins: rubygems 5000
- producers: ustar 4962, none 38
- compression: gzip 5000
- scanner stopped early: 0

## untar

Rejects 6 of 5000 (0.1%); 2 of 2500 latest versions (0.1%).

| reason | tarballs | latest | origins | producers | examples |
|---|---:|---:|---|---|---|
| FileExistsError: [Errno N] File exists: '…' | 4 | 1 | rubygems 4 | ustar 4 | amar-tui@2.1.6; EliteJournal@1.9.480; wreq@1.2.7 |
| Archive contains unsafe path … | 1 | 1 | rubygems 1 | ustar 1 | hello_ST@0.1.0 |
| Archive contains non-directory lib/ named like a directory | 1 | 0 | rubygems 1 | ustar 1 | JEG2-rrdb@0.0.2 |

## Features

Number of tarballs with each feature, of which latest versions; their origins, producers and median mtime years, and what untar did with them.

| feature | tarballs | latest | origins | producers | years | untar rejects | examples |
|---|---:|---:|---|---|---|---:|---|
| `ustar.prefix` | 66 | 37 | rubygems 66 | ustar 66 | 1970–2025 | 0 | second_curtain@0.6.0 `ASHViewControllerSpec/a_view_controller_with_a_loaded_view_s`; impermium@1.1.0 `blog_post_object/blog_post_analyst_feedback_method/missing_a` |
| `name.fills-field` | 40 | 23 | rubygems 40 | ustar 40 | 1970–2025 | 0 | impermium@1.1.0 `cassettes/content_API_section/blog_post_object/blog_post_use`; tinyerp_ruby@0.4.6 `spec/support/vcr/TinyerpRuby_Service/accepts/_lista_atualiza` |
| `name.leading-dot-slash` | 18 | 10 | rubygems 18 | ustar 18 | 1970–2026 | 4 | echolor@0.1.0 `./echolor`; long-decimal@1.00.04 `./Gemfile` |
| `platform.case-collision` | 4 | 2 | rubygems 4 | ustar 4 | 1970–2025 | 0 | bard-file_field@0.1.6 `dummy/features/support/fixtures/empty.jpeg`; jruby-bundler@0.9.7 `spec/project/settings.xml` |
| `tree.duplicate.file-file` | 4 | 1 | rubygems 4 | ustar 4 | 1970–2026 | 4 | amar-tui@2.1.6 `amar-tui.rb`; EliteJournal@1.9.480 `./elitejournal` |
| `name.control-character` | 2 | 1 | rubygems 2 | ustar 2 | 1970–2016 | 0 | fenton_shell@0.1.0 `lib/Icon`; deja-vu@0.4 `example-playback/repo/recordings/DejaVuNS/Recording/bah7aa==` |
| `platform.windows-invalid-character` | 2 | 1 | rubygems 2 | ustar 2 | 1970–2016 | 0 | fenton_shell@0.1.0 `lib/Icon`; deja-vu@0.4 `example-playback/repo/recordings/DejaVuNS/Recording/bah7aa==` |
| `linkname.no-nul` | 1 | 1 | rubygems 1 | ustar 1 | 2015–2015 | 0 | xlmydsykwnrfbnvjffqcokoorkbskzzhrtgnzxkapmjtffjfkwcvwklmsrzwfiatwigrvmftpbybbeqi@0.1.0 `VERSION_FOR_HUMANS` |
| `name.absolute` | 1 | 1 | rubygems 1 | ustar 1 | 2016–2016 | 1 | hello_ST@0.1.0 `/home/tata/hello_ST/lib/hello_ST.rb` |
| `name.trailing-slash-on-file` | 1 | 0 | rubygems 1 | ustar 1 | 1970–1970 | 1 | JEG2-rrdb@0.0.2 `lib/` |
| `platform.windows-trailing-dot-or-space` | 1 | 1 | rubygems 1 | ustar 1 | 2023–2023 | 0 | tamtam-vagrant-reload@1.2.1 `spec/tamtam-vagrant-reload-plugin/config_spec.rb ` |

## Fingerprints

- magic (tarballs using each): posix 4962
- size (tarballs using each): dn 4962
- mode (tarballs using each): dn 4962
- checksum (tarballs using each): dns 4962
- pax_header_name (tarballs using each): 
- extended_sequence (tarballs using each): - 4962
- gnu_long_name (tarballs using each): 
- end (tarballs using each): unpadded 4753, padded-to-10240 247
- zero_blocks_after_end (tarballs using each): 0 5000
- pax_keys (tarballs using each): 
- pax_global_keys (tarballs using each): 
- compression layer: 

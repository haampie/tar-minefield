# Scan of a sample of 10000 PyPI sdists

- tarballs: 10000, scanned: 10000 (5000 latest versions, 5000 older)
- not downloaded: 0, scanner crashed: 0
- downloaded from the first of their URLs (a mirror): 10000
- copied from other scans with `--reuse`: 0, read from `--cache`: 0; sources by host: files.pythonhosted.org 10000
- size: 7.9 GB compressed
- origins: pypi 10000
- producers: Python tarfile (pax) 5759, GNU format 2584, ustar 1648, GNU tar (pax) 8, git archive 1
- compression: gzip 9992, bzip2 8
- scanner stopped early: 0

## untar

Rejects 7 of 10000 (0.1%); 3 of 5000 latest versions (0.1%).

| reason | tarballs | latest | origins | producers | examples |
|---|---:|---:|---|---|---|
| Archive contains unsafe path … | 4 | 2 | pypi 4 | ustar 3, Python tarfile (pax) 1 | spdk@26.9; claude-code-relay@0.0.9; boldi-cli@0.9.4 |
| FileExistsError: [Errno N] File exists: '…' | 3 | 1 | pypi 3 | Python tarfile (pax) 3 | django-mailman3@1.3.15; django-languages-plus@1.1.1; apache-airflow-core@3.3.0 |

## Features

Number of tarballs with each feature, of which latest versions; their origins, producers and median mtime years, and what untar did with them.

| feature | tarballs | latest | origins | producers | years | untar rejects | examples |
|---|---:|---:|---|---|---|---:|---|
| `name.fills-field` | 333 | 161 | pypi 333 | Python tarfile (pax) 260, GNU format 60, ustar 13 | 1970–2026 | 1 | gosce-postgres-kafka-stack-generator@0.1.0 `gosce_postgres_kafka_stack_generator-0.1.0/gosce_postgres_ka`; ntia-conformance-checker@6.0.0 `ntia_conformance_checker-6.0.0/tests/data/missing_component_` |
| `number.gid.no-digits` | 212 | 113 | pypi 212 | GNU format 197, ustar 15 | 1970–2025 | 0 | nav-union@0.1.13 `nav_union-0.1.13/PKG-INFO`; vollama@0.1.0 `vollama-0.1.0/PKG-INFO` |
| `number.uid.no-digits` | 212 | 113 | pypi 212 | GNU format 197, ustar 15 | 1970–2025 | 0 | nav-union@0.1.13 `nav_union-0.1.13/PKG-INFO`; vollama@0.1.0 `vollama-0.1.0/PKG-INFO` |
| `tree.dir-after-contents` | 150 | 89 | pypi 150 | GNU format 140, GNU tar (pax) 8, ustar 2 | 1970–2016 | 0 | nav-union@0.1.13 `nav_union-0.1.13/`; vollama@0.1.0 `vollama-0.1.0/` |
| `name.dir-without-trailing-slash` | 148 | 87 | pypi 148 | GNU format 140, GNU tar (pax) 8 | 1970–1970 | 0 | nav-union@0.1.13 `nav_union-0.1.13/src`; vollama@0.1.0 `vollama-0.1.0/src` |
| `type.nul` | 75 | 41 | pypi 75 | GNU format 75 | 1970–2025 | 0 | annihilation-llm@1.3.0 `annihilation_llm-1.3.0/PKG-INFO`; reaction-system@0.1.4 `reaction_system-0.1.4/Cargo.toml` |
| `number.uid.base256` | 57 | 26 | pypi 57 | GNU format 57 | 2009–2026 | 0 | ride@0.7.2 `ride-0.7.2/`; helloworld-notha99y@0.0.1 `helloworld-notha99y-0.0.1/` |
| `number.gid.base256` | 47 | 22 | pypi 47 | GNU format 47 | 2009–2023 | 0 | ride@0.7.2 `ride-0.7.2/`; helloworld-notha99y@0.0.1 `helloworld-notha99y-0.0.1/` |
| `name.non-ascii` | 26 | 9 | pypi 26 | Python tarfile (pax) 24, GNU tar (pax) 1, GNU format 1 | 1970–2026 | 0 | tuf@7.0.1 `tuf-7.0.1/tests/repository_data/fishy_rolenames/metadata/1.ö`; test-tele@0.0.4.9.9.8 `test_tele-0.0.4.9.9.8/test_tele/web_ui/0_👋_Hello.py` |
| `name.dot` | 22 | 10 | pypi 22 | GNU format 16, Python tarfile (pax) 6 | 2012–2023 | 0 | RFID-UUID-USB-Card-Reader@0.1.1.linux-armv7l `./`; parsl-dag-vis@0.1.6.macosx-10.12-x86_64 `./` |
| `name.leading-dot-slash` | 22 | 10 | pypi 22 | GNU format 16, Python tarfile (pax) 6 | 2012–2023 | 0 | RFID-UUID-USB-Card-Reader@0.1.1.linux-armv7l `./`; parsl-dag-vis@0.1.6.macosx-10.12-x86_64 `./` |
| `platform.case-collision` | 9 | 2 | pypi 9 | Python tarfile (pax) 3, ustar 3, GNU format 3 | 2015–2026 | 0 | pytosql@0.1.0 `pytosql-0.1.0/ChangeLog`; ikiapikit@0.1.0 `ikiapikit-0.1.0/README.md` |
| `pax.size-on-dir` | 8 | 6 | pypi 8 | GNU tar (pax) 8 | 1970–1970 | 0 | anibridge-mal-provider@0.2.3 `anibridge_mal_provider-0.2.3/`; sofias-sdk-lite@0.4.0 `sofias_sdk_lite-0.4.0/` |
| `ustar.prefix` | 8 | 6 | pypi 8 | ustar 7, GNU tar (pax) 1 | 1970–2016 | 0 | polars-bio@0.36.2 `all_operations_speedup_comparison.png`; modbus-rs@0.16.0 `vite.config.ts.timestamp-1783416518050-6e48dfd9640308.mjs` |
| `platform.windows-invalid-character` | 5 | 5 | pypi 5 | Python tarfile (pax) 4, GNU format 1 | 2015–2026 | 0 | lnk@0.1.4 `lnk-0.1.4/tests/bitly/*REPL* [python].py`; SetAnubis@1.0.0 `setanubis-1.0.0/Docs/assets/set-anubis-architecture.jpg:Zone` |
| `name.dotdot` | 4 | 2 | pypi 4 | ustar 3, Python tarfile (pax) 1 | 2020–2023 | 4 | spdk@26.9 `spdk-26.9/../scripts/rpc.py`; claude-code-relay@0.0.9 `claude_code_relay-0.0.9/../README.md` |
| `linkname.no-nul` | 3 | 1 | pypi 3 | Python tarfile (pax) 3 | 2020–2020 | 0 | pyDACP@1.0.1 `pydacp-1.0.1/micromamba/pkgs/asttokens-2.4.1-pyhd8ed1ab_0/si`; oso-semantic@0.1.3a1 `oso_semantic-0.1.3a1/.pyodide_build/pywasmcross_symlinks/ar` |
| `symlink.absolute` | 3 | 1 | pypi 3 | Python tarfile (pax) 2, ustar 1 | 2020–2020 | 0 | fishbowl_inventory@0.0.3 `fishbowl_inventory-0.0.3/venv/bin/python3`; oso-semantic@0.1.3a1 `oso_semantic-0.1.3a1/.pyodide_build/pywasmcross_symlinks/ar` |
| `tree.duplicate.file-file` | 3 | 1 | pypi 3 | Python tarfile (pax) 3 | 2020–2026 | 3 | django-mailman3@1.3.15 `django_mailman3-1.3.15/COPYING.txt`; django-languages-plus@1.1.1 `django-languages-plus-1.1.1/LICENSE` |
| `name.backslash` | 2 | 1 | pypi 2 | Python tarfile (pax) 2 | 2025–2026 | 0 | sdb-debugger@0.6.0 `sdb_debugger-0.6.0/tests/integration/data/regression_output/`; rougail-base@1.2.0 `rougail_base-1.2.0/tests/dictionaries_old/01base_file_utfcha` |
| `symlink.escapes` | 2 | 1 | pypi 2 | ustar 1, Python tarfile (pax) 1 | 2020–2020 | 0 | proteomics-runtime@0.3.8 `proteomics_runtime-0.3.8/LICENSE`; snowpark-checkpoints@0.1.0rc1 `snowpark_checkpoints-0.1.0rc1/snowflake/snowpark_checkpoints` |
| `platform.windows-reserved-name` | 1 | 0 | pypi 1 | GNU format 1 | 2019–2019 | 0 | myssh@0.1.0 `myssh-0.1.0/bin/con` |
| `platform.windows-trailing-dot-or-space` | 1 | 1 | pypi 1 | Python tarfile (pax) 1 | 2026–2026 | 0 | sdb-debugger@0.6.0 `sdb_debugger-0.6.0/tests/integration/data/regression_output/` |

## Fingerprints

- magic (tarballs using each): posix 7416, gnu 2585
- size (tarballs using each): dn 9977, ds 23
- mode (tarballs using each): dn 9977, dsn 23
- checksum (tarballs using each): dns 9758, dn 242
- pax_header_name (tarballs using each): ././@PaxHeader 5759, PaxHeaders/* 8
- extended_sequence (tarballs using each): x 5767, - 4904, L 134
- gnu_long_name (tarballs using each): ././@LongLink 134
- end (tarballs using each): padded-to-10240 9738, unpadded 262
- zero_blocks_after_end (tarballs using each): 0 764, 13 545, 11 513, 10 506, 16 504, 4 503, 19 500, 1 497, 2 491, 6 488, 8 484, 12 483
- pax_keys (tarballs using each): mtime 5600, path 535, uid 36, gid 29, size 8, linkpath 2, uname 1
- pax_global_keys (tarballs using each): comment 1
- compression layer: 

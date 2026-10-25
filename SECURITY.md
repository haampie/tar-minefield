# Security

Cases like those in this test suite have exposed vulnerabilities in tar implementations, such as:

- [CVE-2025-62518](https://github.com/advisories/GHSA-j5gw-2vrg-8fgx): PAX header
  desynchronization in astral-tokio-tar
- [CVE-2025-4517](https://github.com/advisories/GHSA-6r6c-684h-9j7p): writes outside the extraction
  directory in Python's `tarfile`, with `filter="data"`
- [CVE-2021-37701](https://github.com/advisories/GHSA-9r2w-394v-53qc): file creation through
  symlinks in node-tar
- [CVE-2007-4559](https://github.com/advisories/GHSA-gw9q-c7gh-j9vm): directory traversal in
  Python's `tarfile`

If a case shows something like this in an implementation, report it privately to that project
first, as its security policy says. Open an issue or pull request here only once it is fixed or
disclosed. Every project has its own threat model: what is a vulnerability in one can be documented
behavior in another, and the project decides.

If a case affects several projects, or you don't know whom to tell,
[report it here privately](https://github.com/haampie/tar-minefield/security/advisories/new). If
the comparison shows a vulnerability in your project that isn't disclosed yet, report it the same
way, and its results are left out until it is.
